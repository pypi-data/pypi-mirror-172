import asyncio
import logging
import typing

import aio_pika
import aiormq
from aio_pika import ExchangeType
from aio_pika.abc import (
    AbstractRobustExchange,
    AbstractRobustQueue,
    AbstractIncomingMessage,
    AbstractQueue,
)
from aiormq.abc import ConfirmationFrameType

from sparta.rabbit.connection import RabbitMQConnectionProvider

OnMessageSync = typing.Callable[[AbstractIncomingMessage], typing.Any]
OnMessageAsync = typing.Coroutine[typing.Any, typing.Any, AbstractIncomingMessage]
OnMessage = typing.Union[OnMessageSync, OnMessageAsync]


def _to_bytes(message: typing.Union[str, bytes, bytearray]) -> bytes:
    _bytes = message
    if isinstance(message, str):
        return message.encode("utf-8")
    elif isinstance(message, bytearray):
        return bytes(message)


async def _await_if_necessary(anything):
    if asyncio.iscoroutine(anything) or asyncio.iscoroutinefunction(anything):
        return await anything
    else:
        return anything


class RabbitMQClient(object):
    def __init__(self, conn_provider: RabbitMQConnectionProvider):
        self.conn_provider = conn_provider
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    async def close(self) -> None:
        await self.conn_provider.close()

    async def create_exchange(
        self, exchange_name: str, exchange_type: ExchangeType, **kwargs
    ) -> AbstractRobustExchange:
        async with await self.conn_provider.open_channel() as channel:
            return await channel.declare_exchange(
                name=exchange_name, type=exchange_type, **kwargs
            )

    async def delete_exchange(
        self, exchange_name: str, **kwargs
    ) -> aiormq.spec.Exchange.DeleteOk:
        async with await self.conn_provider.open_channel() as channel:
            self.logger.info(f"Deleting exchange {exchange_name}")
            return await channel.exchange_delete(exchange_name=exchange_name, **kwargs)

    async def create_queue(self, queue_name: str, **kwargs) -> AbstractRobustQueue:
        async with await self.conn_provider.open_channel() as channel:
            return await channel.declare_queue(name=queue_name, **kwargs)

    async def purge_queue(self, queue_name: str, **kwargs) -> aiormq.spec.Queue.PurgeOk:
        async with await self.conn_provider.open_channel() as channel:
            queue = await channel.get_queue(name=queue_name)
            self.logger.info(f"Purging queue {queue.name}")
            return await queue.purge(**kwargs)

    async def delete_queue(
        self, queue_name: str, **kwargs
    ) -> aiormq.spec.Queue.DeleteOk:
        async with await self.conn_provider.open_channel() as channel:
            self.logger.info(f"Deleting queue {queue_name}")
            return await channel.queue_delete(queue_name=queue_name, **kwargs)

    async def publish_to_exchange(
        self,
        exchange_name: str,
        message: typing.Union[str, bytes, bytearray],
        routing_key: str = "",
    ) -> typing.Optional[ConfirmationFrameType]:
        async with await self.conn_provider.open_channel() as channel:
            exchange = await channel.get_exchange(exchange_name)
            self.logger.info(f"Publishing to exchange {exchange.name} >> {message}")
            return await exchange.publish(
                message=aio_pika.Message(body=_to_bytes(message)),
                routing_key=routing_key,
            )

    async def publish_to_queue(
        self,
        queue_name: str,
        message: typing.Union[str, bytes, bytearray],
    ) -> typing.Optional[ConfirmationFrameType]:
        async with await self.conn_provider.open_channel() as channel:
            queue = await channel.get_queue(queue_name)
            self.logger.info(f"Publishing to queue {queue.name} >> {message}")
            return await channel.default_exchange.publish(
                message=aio_pika.Message(body=_to_bytes(message)),
                routing_key=queue.name,
            )

    async def listen_to_exchange(
        self,
        exchange_name: str,
        on_message: typing.Callable[[AbstractIncomingMessage], typing.Any],
        **kwargs,
    ) -> None:
        async with await self.conn_provider.open_channel() as channel:
            exchange = await channel.get_exchange(exchange_name)
            queue = await channel.declare_queue(exclusive=True)
            await queue.bind(exchange)
            self.logger.info(f"Listening to exchange {exchange_name} ...")
            await self._consume_queue(queue, on_message, **kwargs)

    async def listen_to_queue(
        self,
        queue_name: str,
        on_message: OnMessage,
        **kwargs,
    ) -> None:
        async with await self.conn_provider.open_channel() as channel:
            queue = await channel.get_queue(queue_name)
            self.logger.info(f"Listening to queue {queue_name} ...")
            await self._consume_queue(queue, on_message, **kwargs)

    async def _consume_queue(
        self,
        queue: AbstractQueue,
        on_message: OnMessage,
        **kwargs,
    ) -> None:
        try:
            async with queue.iterator(**kwargs) as _iter:
                async for message in _iter:
                    try:
                        message = await _await_if_necessary(message)
                        await _await_if_necessary(on_message(message))
                    except Exception as e:
                        self.logger.error(
                            f"Error processing message {message.message_id}"
                        )
                        self.logger.exception(e)
        except (
            TimeoutError,
            asyncio.exceptions.TimeoutError,
        ):
            self.logger.warning(f"Listening to queue '{queue.name}' timed-out!")
        except asyncio.exceptions.CancelledError:
            self.logger.warning(f"Listening to queue '{queue.name}' was cancelled!")
