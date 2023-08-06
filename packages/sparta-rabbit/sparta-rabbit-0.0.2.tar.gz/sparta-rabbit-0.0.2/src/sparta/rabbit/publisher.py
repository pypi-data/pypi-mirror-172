import typing

import aio_pika
from aiormq.abc import ConfirmationFrameType

from sparta.rabbit.base_client import RabbitMQBaseClient
from sparta.rabbit.connection import RabbitMQConnectionProvider


def _to_bytes(message: typing.Union[str, bytes, bytearray]) -> bytes:
    _bytes = message
    if isinstance(message, str):
        return message.encode("utf-8")
    elif isinstance(message, bytearray):
        return bytes(message)


class RabbitMQPublisher(RabbitMQBaseClient):
    def __init__(self, conn_provider: RabbitMQConnectionProvider):
        super().__init__(conn_provider)
        self.logger.debug("New instance")

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
