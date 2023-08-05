import contextlib

from dependency_injector import containers, providers

from dropland.app.base import ContainerBlock, SessionResourceBlock
from dropland.data.context import get_context
from dropland.util import default_value
from .engine import EngineConfig, SqlStorageBackend
from .session import SessionManager


class SqlBlock(ContainerBlock, SessionResourceBlock):
    def sync_startup(self, *args, **kwargs):
        if self.initialized:
            return
        self.container.init_resources()
        self._initialized = True

    def sync_shutdown(self, *args, **kwargs):
        if not self.initialized:
            return
        self.container.shutdown_resources()
        self._initialized = False

    async def startup(self, *args, **kwargs):
        if self.initialized:
            return
        await self.container.init_resources()
        self._initialized = True

    async def shutdown(self, *args, **kwargs):
        if not self.initialized:
            return
        await self.container.shutdown_resources()
        self._initialized = False

    def sync_session_begin(self, begin_tx: bool = True, autocommit: bool = True, *args, **kwargs):
        ctx = get_context()
        if not self.initialized or '_sql_sync_block' in ctx:
            return

        ctx._sql_sync_block = contextlib.ExitStack().__enter__()
        for name, engine in self.container.engine_factory().get_engines().items():
            if not engine.is_async:
                ctx._sql_sync_block.enter_context(
                    self.container.manager().sync_session_context(name, begin_tx=begin_tx, autocommit=autocommit)
                )

    def sync_session_finish(self, *args, **kwargs):
        ctx = get_context()
        if not self.initialized or '_sql_sync_block' not in ctx:
            return

        ctx._sql_sync_block.__exit__(None, None, None)
        del ctx._sql_sync_block

    async def session_begin(self, begin_tx: bool = True, autocommit: bool = True, *args, **kwargs):
        ctx = get_context()
        if not self.initialized or '_sql_block' in ctx:
            return

        ctx._sql_block = await contextlib.AsyncExitStack().__aenter__()
        for name, engine in self.container.engine_factory().get_engines().items():
            if engine.is_async:
                await ctx._sql_block.enter_async_context(
                    self.container.manager().session_context(name, begin_tx=begin_tx, autocommit=autocommit)
                )

    async def session_finish(self, *args, **kwargs):
        ctx = get_context()
        if not self.initialized or '_sql_block' not in ctx:
            return

        await ctx._sql_block.__aexit__(None, None, None)
        del ctx._sql_block

    def get_engine(self, *args, **kwargs):
        if isinstance(self.container, SingleSqlStorage) or 'SingleSqlStorage' == self.container.parent_name:
            return self.container.create_engine()
        return self.container.create_engine(*args, **kwargs)

    def get_session(self, *args, **kwargs):
        if isinstance(self.container, SingleSqlStorage) or 'SingleSqlStorage' == self.container.parent_name:
            return self.container.get_session()
        return self.container.get_session(*args, **kwargs)


class SqlStorage(containers.DeclarativeContainer):
    __self__ = providers.Self()
    engine_factory = providers.Singleton(SqlStorageBackend)
    manager = providers.Singleton(SessionManager, engine_factory)

    def _create_engine(self, *args, **kwargs):
        return self.engine_factory().create_engine(*args, **kwargs)

    def _init_sync_session(self):
        with self.manager().init_sync_engines():
            yield self.manager()

    async def _init_session(self):
        async with self.manager().init_engines():
            yield self.manager()

    create_engine = providers.Factory(_create_engine, __self__)
    sync_session_context = providers.Resource(_init_sync_session, __self__)
    session_context = providers.Resource(_init_session, __self__)
    get_session = providers.Factory(manager.provided.get_session.call())
    block = providers.Singleton(SqlBlock, __self__)

    wiring_config = containers.WiringConfiguration(
        modules=['.model']
    )


class SingleSqlStorage(SqlStorage):
    __self__ = providers.Self()
    config = providers.Configuration()

    def _create_engine(self):
        if isinstance(self.config.engine_config(), EngineConfig):
            engine_config = self.config.engine_config()
        else:
            engine_config = EngineConfig(
                url=self.config.engine_config.url(),
                echo=self.config.engine_config.echo.as_(bool)(),
                pool_min_size=self.config.engine_config.
                    pool_min_size.as_(default_value(int))(default=1),
                pool_max_size=self.config.engine_config.
                    pool_max_size.as_(default_value(int))(default=8),
                pool_expire_seconds=self.config.engine_config.
                    pool_expire_seconds.as_(default_value(int))(default=60),
                pool_timeout_seconds=self.config.engine_config.
                    pool_timeout_seconds.as_(default_value(int))(default=15)
            )
        return SqlStorage._create_engine(
            self, self.config.name(), engine_config, self.config.db_type(),
            use_async=self.config.use_async.as_(bool)())

    create_engine = providers.Factory(_create_engine, __self__)
    sync_session_context = providers.Resource(SqlStorage._init_sync_session, __self__)
    session_context = providers.Resource(SqlStorage._init_session, __self__)
    get_session = providers.Factory(SqlStorage.get_session, config.name)
    block = providers.Singleton(SqlBlock, __self__)

    wiring_config = containers.WiringConfiguration(
        modules=['.model']
    )


class MultipleSqlStorage(SqlStorage):
    __self__ = providers.Self()
    config = providers.Configuration()

    def _create_engine(self, name: str):
        if conf := self.config.get(name):
            if isinstance(conf['engine_config'], EngineConfig):
                engine_config = conf['engine_config']
            else:
                engine_config = EngineConfig(
                    url=conf['engine_config']['url'],
                    echo=bool(conf['engine_config'].get('echo')),
                    pool_min_size=int(conf['engine_config'].get('pool_min_size', 1)),
                    pool_max_size=int(conf['engine_config'].get('pool_max_size', 8)),
                    pool_expire_seconds=int(conf['engine_config'].get('pool_expire_seconds', 60)),
                    pool_timeout_seconds=int(conf['engine_config'].get('pool_timeout_seconds', 15))
                )
            return SqlStorage._create_engine(
                self, name, engine_config, conf['db_type'], use_async=conf.get('use_async', False))
        return None

    def _get_session(self, name: str):
        return self.manager().get_session(name)

    create_engine = providers.Factory(_create_engine, __self__)
    sync_session_context = providers.Resource(SqlStorage._init_sync_session, __self__)
    session_context = providers.Resource(SqlStorage._init_session, __self__)
    get_session = providers.Factory(_get_session, __self__)
    block = providers.Singleton(SqlBlock, __self__)

    wiring_config = containers.WiringConfiguration(
        modules=['.model']
    )
