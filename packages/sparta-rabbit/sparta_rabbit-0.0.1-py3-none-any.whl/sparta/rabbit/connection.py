import asyncio
import dataclasses
import logging
import threading
import typing
from types import TracebackType
from typing import Optional, Any, Type

import aio_pika
from aio_pika import RobustConnection
from aio_pika.abc import (
    AbstractRobustConnection,
    AbstractRobustChannel,
)
from yarl import URL


@dataclasses.dataclass
class RabbitMQConnectionData:
    host: str
    port: int = 5672
    username: str = None
    password: str = None
    vhost: str = "/"
    _url: str = None

    @property
    def connection_string(self):
        if not self._url:
            # TODO encode self.vhost
            if self.username is not None and self.password is not None:
                self._url = f"amqp://{self.username}:{self.password}@{self.host}:{self.port}/{self.vhost}"
            else:
                self._url = f"amqp://{self.host}:{self.port}/{self.vhost}"
        return self._url

    @property
    def connection_string_masked(self):
        return self.connection_string.replace(f"{self.username}:{self.password}", "***")


class _RobustConnectionIgnoreAExit(RobustConnection):
    def __init__(
        self, url: URL, loop: Optional[asyncio.AbstractEventLoop] = None, **kwargs: Any
    ):
        super().__init__(url, loop, **kwargs)

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        pass


class RabbitMQConnectionProvider:
    def __init__(
        self,
        conn_data: RabbitMQConnectionData,
    ):
        self._conn_data = conn_data
        self._conn: typing.Optional[AbstractRobustConnection] = None
        self._get_loop = lambda: asyncio.get_running_loop()
        self._lock = threading.Lock()
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.logger.debug("New instance")

    async def __aenter__(
        self,
    ) -> "RabbitMQConnectionProvider":
        return self

    async def __aexit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_val: typing.Optional[BaseException],
        exc_tb: typing.Optional[TracebackType],
    ) -> None:
        await self.close()

    async def close(self) -> None:
        if self._conn and not self._conn.is_closed:
            with self._lock:
                if self._conn and not self._conn.is_closed:
                    self.logger.info(
                        f"Closing connection to RabbitMQ on {self._conn_data.connection_string_masked}"
                    )
                    await self._conn.close()

    async def _on_connection_close(self, *args, **kwargs) -> None:
        self.logger.debug("Connection closed")

    async def _on_connection_reconnect(self, *args, **kwargs) -> None:
        self.logger.debug("Reconnected")

    async def open_channel(self, **kwargs) -> AbstractRobustChannel:
        con = await self.reuse_connection()
        return con.channel(**kwargs)

    async def reuse_connection(self) -> AbstractRobustConnection:
        if not self._conn or self._conn.is_closed:
            with self._lock:
                if not self._conn or self._conn.is_closed:
                    self._conn = await self.open_connection(
                        connection_class=_RobustConnectionIgnoreAExit
                    )
        return self._conn

    async def open_connection(
        self, connection_class: Type[AbstractRobustConnection] = RobustConnection
    ) -> AbstractRobustConnection:
        try:
            self.logger.debug(
                f"Connecting to RabbitMQ on {self._conn_data.connection_string_masked}"
            )
            return await aio_pika.connect_robust(
                self._conn_data.connection_string,
                loop=self._get_loop(),
                connection_class=connection_class,
            )
        finally:
            self.logger.info(
                f"Connected to RabbitMQ on {self._conn_data.connection_string_masked}"
            )
