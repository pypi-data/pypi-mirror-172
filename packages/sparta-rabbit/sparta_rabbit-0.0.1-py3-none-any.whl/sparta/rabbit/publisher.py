import typing

import aio_pika
from aiormq.abc import ConfirmationFrameType

from sparta.rabbit.base_client import RabbitMQBaseClient
from sparta.rabbit.connection import RabbitMQConnectionProvider


class RabbitMQPublisher(RabbitMQBaseClient):
    def __init__(self, conn_provider: RabbitMQConnectionProvider):
        super().__init__(conn_provider)
        self.logger.debug("New instance")

    async def publish_to_exchange(
        self,
        exchange_name: str,
        message: str,
        routing_key: str = "",
        declare_exchange_if_missing=False,
        declare_exchange_kwargs: typing.Optional[dict] = None,
    ) -> typing.Optional[ConfirmationFrameType]:
        async with await self.conn_provider.open_channel() as channel:
            exchange = await self.get_exchange(
                channel,
                exchange_name,
                declare_exchange_if_missing,
                **(declare_exchange_kwargs or {}),
            )
            self.logger.info(f"Publishing to exchange {exchange.name} >> {message}")
            return await exchange.publish(
                message=aio_pika.Message(body=message.encode("utf-8")),
                routing_key=routing_key,
            )

    async def publish_to_queue(
        self,
        queue_name: str,
        message: str,
        declare_queue_if_missing=False,
        declare_queue_kwargs: typing.Optional[dict] = None,
    ) -> typing.Optional[ConfirmationFrameType]:
        async with await self.conn_provider.open_channel() as channel:
            queue = await self.get_queue(
                channel,
                queue_name,
                declare_queue_if_missing,
                **(declare_queue_kwargs or {}),
            )
            self.logger.info(f"Publishing to queue {queue.name} >> {message}")
            return await channel.default_exchange.publish(
                message=aio_pika.Message(body=message.encode("utf-8")),
                routing_key=queue.name,
            )
