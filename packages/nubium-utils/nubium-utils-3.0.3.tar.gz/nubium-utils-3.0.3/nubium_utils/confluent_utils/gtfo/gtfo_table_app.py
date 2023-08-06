from confluent_kafka import TopicPartition, KafkaException
from nubium_utils.custom_exceptions import NoMessageError
from nubium_utils.confluent_utils.confluent_configs import init_schema_registry_configs, env_vars
from .rocksdb_utils import RDB, RdbTableInUse
from .gtfo_app import GtfoApp, Transaction
import logging
from time import sleep
from json import dumps, loads
from copy import deepcopy
from collections import deque
# TODO: consider using orjson for changelog speed increases?
# from orjson import dumps, loads
# changelog_schema = {"type": "bytes"}
changelog_schema = {"type": "string"}


LOGGER = logging.getLogger(__name__)


class PartitionsAssigned(Exception):
    def __init__(self):
        pass


class TableTransaction(Transaction):
    def __init__(self, producer, consumer, app_changelog_topic, app_tables, metrics_manager=None, message=None, auto_consume=True, timeout=5, parent_app=None):
        self.app_changelog_topic = app_changelog_topic
        self.app_tables = app_tables
        self._changelog_updated = False
        self._pending_table_write = None
        super().__init__(producer, consumer, metrics_manager=metrics_manager, message=message, auto_consume=auto_consume, timeout=timeout, parent_app=parent_app)

    def _refresh_transaction_fields(self):
        super()._refresh_transaction_fields()
        self._changelog_updated = False
        self._pending_table_write = None

    def read_table_entry(self):
        return self._table_read()

    def update_table_entry(self, value, mark_changelog_updated=True):
        self._pending_table_write = deepcopy(value)
        if isinstance(self._pending_table_write, (list, dict)):
            self._pending_table_write = dumps(self._pending_table_write)
        self._update_changelog(mark_updated=mark_changelog_updated)

    def delete_table_entry(self):
        self._pending_table_write = '-DELETED-'

    def _update_changelog(self, mark_updated=True):
        if not self._changelog_updated and self._pending_table_write:
            LOGGER.debug('Updating changelog topic...')
            self.produce(dict(
                topic=self.app_changelog_topic,
                key=self.key(),
                value=self._pending_table_write,
                partition=self.partition()
            ))
            self._changelog_updated = mark_updated
            self.producer.poll(0)

    def _recover_table_via_changelog(self):
        self._changelog_updated = True  # so we dont produce a message back to the changelog
        value = self.value()
        try:
            value = loads(value)
        except:
            pass
        LOGGER.debug(f'TABLE VALUE:\n{value}')
        if value == '-DELETED-':
            self.delete_table_entry()
        else:
            self.update_table_entry(value)

    def _table_write(self, partition=None):
        """
        Partition arg generally only used by subclasses
        """
        # TODO: have this share objects with autobatch to consolidate logic
        if partition is None:
            partition = self.partition()
        if self._pending_table_write:
            if self._pending_table_write == '-DELETED-':
                LOGGER.debug('Finalizing table entry delete...')
                self.app_tables[partition].delete(self.key())
                self.app_tables[partition].write('offset', str(self._table_offset(partition=partition) + 2))
            else:
                LOGGER.debug(f'Finalizing table entry write:\npartition{partition}, key:{self.key()}')
                self.app_tables[self.partition()].write_batch(
                    {self.key(): self._pending_table_write,
                     'offset': str(self._table_offset(partition=partition) + 2)})
            self._pending_table_write = None

    def _table_read(self, partition=None):
        """
        Partition arg generally only used by subclasses
        """
        if partition is None:
            partition = self.partition()
        value = self.app_tables[partition].read(self.key())
        try:
            value = loads(value)
        except:
            pass
        return value

    def _table_offset(self, partition=None):
        """
        Partition arg generally only used by subclasses
        """
        if partition is None:
            partition = self.partition()
        value = self.app_tables[partition].read('offset')
        return int(value) if value else 0

    def commit(self, mark_committed=True):
        super().commit(mark_committed=mark_committed)
        self._table_write()
        LOGGER.debug('Transaction Committed!')


class GtfoTableApp(GtfoApp):
    def __init__(self, app_function, consume_topic, produce_topic_schema_dict=None, transaction_type=TableTransaction,
                 app_function_arglist=None, metrics_manager=None, schema_registry=None, cluster_name=None, consumer=None, producer=None):
        self.changelog_topic = f"{env_vars()['NU_APP_NAME']}__changelog"
        self.tables = {}
        self._active_primary_partitions = {}
        self._paused_primary_partitions = {}
        self._active_table_changelog_partitions = {}
        self._pending_table_db_assignments = deque()
        self._pending_table_recoveries = {}

        if not produce_topic_schema_dict:
            produce_topic_schema_dict = {}
        if self.changelog_topic not in produce_topic_schema_dict:
            produce_topic_schema_dict.update({self.changelog_topic: changelog_schema})
        if not cluster_name:
            cluster_name = self._get_cluster_name(consume_topic)
        if not schema_registry:
            schema_registry = init_schema_registry_configs()
        if not consumer:
            consumer = self._set_table_consumer(consume_topic, schema_registry, cluster_name=cluster_name)

        self.consume_topic = consume_topic

        super().__init__(
            app_function, self.consume_topic, produce_topic_schema_dict, transaction_type=transaction_type,
            app_function_arglist=app_function_arglist, metrics_manager=metrics_manager, schema_registry=schema_registry, cluster_name=cluster_name, consumer=consumer, producer=producer)

    def _set_table_consumer(self, topic, schema_registry, default_schema=None, cluster_name=None):
        if isinstance(topic, str):
            topic = [topic]
        consumer = self._get_transactional_consumer(topic, schema_registry, cluster_name, default_schema, False)
        consumer.subscribe(topic, on_assign=self._partition_assignment, on_revoke=self._partition_unassignment, on_lost=self._partition_unassignment)
        LOGGER.debug('Consumer initialized.')
        return consumer

    def _table_close(self, partitions=None):
        interrupt = None
        full_shutdown = False
        if not partitions or self._shutdown:
            partitions = list(self.tables.keys())
            full_shutdown = True
        LOGGER.debug(f'Table - closing connections for partitions {partitions}')
        for p in partitions:
            try:
                table = self.tables[p]
                if table.active_lock:
                    LOGGER.debug(f'Closing table db p{p}')
                    self.tables[p].close()
                    sleep(.1)  # try to slow down pvc stuff a little
                LOGGER.debug(f'p{p} table connection closed.')
            except KeyError:
                if not full_shutdown:
                    LOGGER.debug(
                        f'Table p{p} did not seem to be mounted and thus could not unmount,'
                        f' likely caused by multiple rebalances in quick succession.'
                        f' This is unliklely to cause issues as the client is in the middle of adjusting itself, '
                        f' but should be noted.')
            except Exception as e:
                LOGGER.debug(f'Interrupt received during table db closing, {e}')
                interrupt = e
        LOGGER.info(f'RocksDB - closed connections for partitions {partitions}')
        if interrupt:  # ensure all table cleanup happens
            LOGGER.info('Continuing with exception interrupt raised during table closing')
            raise interrupt

    def _partition_assignment(self, consumer, add_partition_objs):
        """
        Called every time a rebalance happens and handles table assignment and recovery flow.
        NOTE: rebalances pass relevant partitions per rebalance call which can happen multiple times, especially when
        multiple apps join at once; we have objects to track all updated partitions received during the entire rebalance.
        NOTE: confluent-kafka expects this method to have exactly these two arguments ONLY
        NOTE: _partition_assignment will ALWAYS be called (even when no new assignments are required) after _partition_unassignment.
            """
        if not self._shutdown:
            self.transaction.abort_active_transaction()
            LOGGER.debug('Rebalance Triggered - Assigment')
            partitions = {p_obj.partition: p_obj for p_obj in add_partition_objs}
            if add_partition_objs:
                LOGGER.info(f'Rebalance - Assigning additional partitions: {list(partitions.keys())}')
                self._paused_primary_partitions.update(partitions)
                self._pending_table_db_assignments.extend(list(partitions.keys()))
                self._pending_table_recoveries.update({p: None for p in partitions.keys()})
                self.consumer.incremental_assign(add_partition_objs)
                self.consumer.pause(add_partition_objs)
                raise PartitionsAssigned  # want to interrupt what it was doing
            else:
                LOGGER.debug(f'No new partitions assigned, skipping rebalance handling')

    def _partition_unassignment(self, consumer, drop_partition_objs):
        """
        NOTE: confluent-kafka expects this method to have exactly these two arguments ONLY
        NOTE: _partition_assignment will always be called (even when no new assignments are required) after _partition_unassignment.
        """
        LOGGER.info('Rebalance Triggered - Unassigment')
        partitions = [p_obj.partition for p_obj in drop_partition_objs]
        self.transaction.abort_active_transaction()
        self._table_close([p for p in self.tables.keys() if p in partitions])
        unassign_active_changelog = {p: p_obj for p, p_obj in self._active_table_changelog_partitions.items() if p in partitions}
        full_unassign = {self.changelog_topic: list(unassign_active_changelog.keys()), self.consume_topic: partitions}
        if self._pending_table_recoveries:
            full_unassign.update({self.changelog_topic: list(unassign_active_changelog.keys())}),

        LOGGER.info(f'Unassigning partitions:\n{full_unassign}')
        self.consumer.incremental_unassign(list(unassign_active_changelog.values()) + drop_partition_objs)

        for var in ['_active_primary_partitions', '_paused_primary_partitions', '_active_table_changelog_partitions', '_pending_table_recoveries']:
            self.__setattr__(var, {k: v for k, v in self.__getattribute__(var).items() if k not in partitions})
            LOGGER.debug(f'{var} after unassignment: {list(self.__getattribute__(var).keys())}')
        self._pending_table_db_assignments = deque([i for i in self._pending_table_recoveries if i not in partitions])
        LOGGER.debug(f'_pending_table_db_assignments after unassignment: {self._pending_table_db_assignments}')
        LOGGER.info('Unassignment Complete!')

    def _pause_active_primary_partitions(self):
        self.consumer.pause(list(self._active_primary_partitions.values()))
        self._paused_primary_partitions.update(self._active_primary_partitions)
        self._active_primary_partitions = {}

    def _resume_active_primary_partitions(self):
        self.consumer.resume(list(self._paused_primary_partitions.values()))
        self._active_primary_partitions.update(self._paused_primary_partitions)
        self._paused_primary_partitions = {}

    def _cleanup_and_resume_app_loop(self):
        if self._active_table_changelog_partitions:
            LOGGER.info(f'unassigning changelog partitions: {list(self._active_table_changelog_partitions.values())}')
            self.consumer.incremental_unassign(list(self._active_table_changelog_partitions.values()))
            self._active_table_changelog_partitions = {}
        LOGGER.debug(f'Resuming consumption for paused topic partitions:\n{list(self._paused_primary_partitions.keys())}')
        self._resume_active_primary_partitions()
        LOGGER.info(f'Continuing normal consumption loop for partitions {list(self._active_primary_partitions.keys())}')

    def _get_changelog_watermarks(self, p_pobj_dict):
        """
        Note: this is a separate function since it requires the consumer to communicate with the broker
        """
        return {p: {'watermarks': self.consumer.get_watermark_offsets(p_obj, timeout=8), 'partition_obj': p_obj} for p, p_obj in p_pobj_dict.items()}

    def _table_recovery_set_offset_seek(self):
        """ Refresh the offsets of recovery partitions to account for updated recovery states during rebalancing """
        for p, offsets in self._pending_table_recoveries.items():
            new_offset = self._pending_table_recoveries[p]['table_offset_recovery']
            low_mark = self._pending_table_recoveries[p]['watermarks'][0]
            if low_mark > new_offset:  # handles offsets that have been removed/compacted. Should never happen, but ya know
                LOGGER.info(
                    f'p{p} table has an offset ({new_offset}) less than the changelog lowwater ({low_mark}), likely due to retention settings. Setting {low_mark} as offset start point.')
                new_offset = low_mark
            high_mark = self._pending_table_recoveries[p]['watermarks'][1]
            LOGGER.debug(f'p{p} table has an offset delta of {high_mark - new_offset}')
            self._pending_table_recoveries[p]['partition_obj'].offset = new_offset

    def _refresh_pending_table_recoveries(self):
        """
        confirms new recoveries and removes old ones if not applicable anymore
        """
        if env_vars()['NU_SKIP_TABLE_RECOVERY'] == 'true':  # DEBUGGING PURPOSES ONLY
            self._pending_table_recoveries = {}
        else:
            partition_watermarks = self._get_changelog_watermarks({p: TopicPartition(topic=self.changelog_topic, partition=int(p)) for p, d in self._pending_table_recoveries.items()})
            for partition, data in partition_watermarks.items():
                watermarks = data['watermarks']
                if watermarks[0] != watermarks[1]:
                    table_offset = self.tables[partition].read('offset')
                    if table_offset:
                        table_offset = int(table_offset)
                    else:
                        table_offset = 0
                    LOGGER.info(f'(lowwater, highwater) [table_offset] for changelog p{partition}: {watermarks}, [{table_offset}]')
                    if table_offset < watermarks[1]:
                        data['table_offset_recovery'] = table_offset
            self._pending_table_recoveries = {k: v for k, v in partition_watermarks.items() if v.get('table_offset_recovery') is not None}
            LOGGER.debug(f'Remaining recoveries after offset refresh check: {self._pending_table_recoveries}')
            self._table_recovery_set_offset_seek()

    def _table_db_init(self, partition, allow_lock_delete=False, sleep_for=0):
        if sleep_for:
            LOGGER.debug(f'Sleeping for {sleep_for} seconds before trying db p{partition} init...')
            sleep(sleep_for)
        rdb = RDB(f'p{partition}', delete_existing_lock=allow_lock_delete)
        self.tables[partition] = rdb  # avoids false success by calling/assigning separately
        LOGGER.info(f'Table p{partition} initialized')

    def _table_db_assignments(self, max_retry=3):
        partition_attempts = {p: 0 for p in self._pending_table_db_assignments}
        while self._pending_table_db_assignments:
            partition = self._pending_table_db_assignments.popleft()
            try:
                if partition not in self.tables:
                    sleep(.1)  # try to slow down pvc stuff a little
                    self._table_db_init(partition, sleep_for=partition_attempts[partition]**2)
            except RdbTableInUse as e:  # waiting for other app instance to relinquish claim on rdb table
                partition_attempts[partition] += 1
                LOGGER.debug(e)
                if partition_attempts[partition] == max_retry:
                    self._table_db_init(partition, allow_lock_delete=True)  # pretty sure this doesn't work.
                else:
                    self._pending_table_db_assignments.append(partition)
            except:
                self._pending_table_db_assignments.append(partition)
                raise

    def _set_table_offset_to_latest(self, partition):
        LOGGER.debug(f'Setting table offset p{partition} to latest')
        self.tables[partition].write('offset', str(self._pending_table_recoveries[partition]['watermarks'][1]))
        del self._pending_table_recoveries[partition]
        LOGGER.info(f'table p{partition} fully recovered!')

    def _table_recovery_loop(self, checks=3):
        while checks and self._pending_table_recoveries:
            try:
                LOGGER.info(f'Consuming from changelog partitions: {list(self._active_table_changelog_partitions.keys())}')
                self.consume()
                self.transaction._recover_table_via_changelog()
                # NOTE: no commit here since its just writing to the table
                p = self.transaction.partition()
                LOGGER.info(f"transaction_offset - {self.transaction.offset() + 2}, watermark - {self._pending_table_recoveries[p]['watermarks'][1]}")
                self.transaction._table_write()
                if self._pending_table_recoveries[p]['watermarks'][1] - (self.transaction.offset() + 2) <= 0:
                    self._set_table_offset_to_latest(p)
            except NoMessageError:
                checks -= 1
                LOGGER.debug(f'No changelog messages, checks remaining: {checks}')
        if not checks:
            for p in list(self._pending_table_recoveries.keys()):  # list stops dict iter size change exception
                self._set_table_offset_to_latest(p)

    def _throwaway_poll(self):
        """ Have to poll (changelog topic) after first assignment to it to allow seeking """
        LOGGER.debug("Performing throwaway poll to allow assignments to properly initialize...")
        try:
            self.consume(timeout=8)
        except NoMessageError:
            pass

    def _assign_recovery_partitions(self):
        # TODO: maybe add additional check/inclusion of assignment based on c.assignment to avoid desync? (hasnt happened yet though)
        LOGGER.debug(f'Preparing changelog table recovery partition assignments...')
        to_assign = {p: self._pending_table_recoveries[p]['partition_obj'] for p in
                     self._pending_table_recoveries.keys() if p not in self._active_table_changelog_partitions}
        LOGGER.info(f'Assigning changelog partitions {to_assign}')
        self._active_table_changelog_partitions.update(to_assign)
        self.consumer.incremental_assign(list(to_assign.values()))  # strong assign due to needing to seek
        LOGGER.debug(f'pending table recoveries before recovery attempt: {list(self._pending_table_recoveries.keys())}')
        LOGGER.debug(f'assigned recoveries before recovery attempt (should match pending now): {self._active_table_changelog_partitions}')

    def _table_recovery_start(self):
        try:
            for partition_info in self._pending_table_recoveries.values():
                self.consumer.seek(partition_info['partition_obj'])
            self._table_recovery_loop()
        except KafkaException as kafka_error:
            if 'Failed to seek to offset' in kafka_error.args[0].str():
                LOGGER.debug('Running a consumer poll to allow seeking to work on the changelog partitions...')
                self._throwaway_poll()
                self._table_recovery_start()
            else:
                raise

    def _table_and_recovery_manager(self):
        try:
            self._table_db_assignments()
            self._refresh_pending_table_recoveries()
            if self._pending_table_recoveries:
                self._pause_active_primary_partitions()
                while self._pending_table_recoveries:
                    self._assign_recovery_partitions()
                    LOGGER.info('BEGINNING TABLE RECOVERY PROCEDURE')
                    self._table_recovery_start()
                    if self._pending_table_recoveries:
                        self._refresh_pending_table_recoveries()
                LOGGER.info("TABLE RECOVERY COMPLETE!")
            else:
                LOGGER.info('No table recovery required!')
            self._cleanup_and_resume_app_loop()
        except PartitionsAssigned:
            LOGGER.info('Rebalance triggered while recovering tables. Will resume recovery after, if needed.')
            self._table_and_recovery_manager()

    def consume(self, *args, **kwargs):
        return super().consume(*args, app_changelog_topic=self.changelog_topic, app_tables=self.tables, **kwargs)

    def _app_run_loop(self, *args, **kwargs):
        LOGGER.info(f'Consuming from partitions: {list(self._active_primary_partitions.keys())}')
        while not self._shutdown:
            try:
                super()._app_run_loop(*args, **kwargs)
            except PartitionsAssigned:
                self._table_and_recovery_manager()

    def _app_shutdown(self):
        super()._app_shutdown()
        self._table_close()
