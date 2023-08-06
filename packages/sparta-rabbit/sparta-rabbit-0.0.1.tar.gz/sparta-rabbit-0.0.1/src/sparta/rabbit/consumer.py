import asyncio
import typing

from aio_pika.abc import AbstractIncomingMessage, AbstractQueue

from sparta.rabbit.base_client import RabbitMQBaseClient
from sparta.rabbit.connection import RabbitMQConnectionProvider


class RabbitMQConsumer(RabbitMQBaseClient):
    def __init__(self, conn_provider: RabbitMQConnectionProvider):
        super().__init__(conn_provider)
        self.logger.debug("New instance")

    async def listen_to_exchange(
        self,
        exchange_name: str,
        on_message: typing.Callable[[AbstractIncomingMessage], typing.Any],
        declare_exchange_if_missing=False,
        declare_exchange_kwargs: typing.Optional[dict] = None,
        **kwargs,
    ) -> None:
        async with await self.conn_provider.open_channel() as channel:
            exchange = await self.get_exchange(
                channel,
                exchange_name,
                declare_exchange_if_missing,
                **(declare_exchange_kwargs or {}),
            )
            queue = await channel.declare_queue(exclusive=True)
            await queue.bind(exchange)
            self.logger.info(f"Listening to exchange {exchange_name} ...")
            await self._consume_queue(queue, on_message, **kwargs)

    async def listen_to_queue(
        self,
        queue_name: str,
        on_message: typing.Union[
            typing.Callable[[AbstractIncomingMessage], typing.Any],
            typing.Coroutine[typing.Any, typing.Any, AbstractIncomingMessage],
        ],
        declare_queue_if_missing=False,
        declare_queue_kwargs: typing.Optional[dict] = None,
        **kwargs,
    ) -> None:
        async with await self.conn_provider.open_channel() as channel:
            queue = await self.get_queue(
                channel,
                queue_name,
                declare_queue_if_missing,
                **(declare_queue_kwargs or {}),
            )
            self.logger.info(f"Listening to queue {queue_name} ...")
            await self._consume_queue(queue, on_message, **kwargs)

    async def _consume_queue(
        self,
        queue: AbstractQueue,
        on_message: typing.Union[
            typing.Callable[[AbstractIncomingMessage], typing.Any],
            typing.Coroutine[typing.Any, typing.Any, AbstractIncomingMessage],
        ],
        **kwargs,
    ) -> None:
        try:
            async with queue.iterator(**kwargs) as _iter:
                async for message in _iter:
                    try:
                        if asyncio.iscoroutine(message) or asyncio.iscoroutinefunction(
                            message
                        ):
                            message = await message
                        if asyncio.iscoroutine(
                            on_message
                        ) or asyncio.iscoroutinefunction(on_message):
                            await on_message(message)
                        else:
                            on_message(message)
                    except Exception as e1:
                        self.logger.error(
                            f"Error processing message {message.message_id} {e1}"
                        )
                        self.logger.exception(e1)
        except asyncio.exceptions.TimeoutError as e2:
            # self.logger.error(f"TimeoutError {e2}")
            # self.logger.exception(e2)
            pass
        except asyncio.exceptions.CancelledError as e3:
            # self.logger.error(f"CancelledError {e3}")
            # self.logger.exception(e3)
            pass
