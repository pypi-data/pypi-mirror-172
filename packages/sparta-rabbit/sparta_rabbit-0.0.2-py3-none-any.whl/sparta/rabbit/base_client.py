import logging

import aiormq
from aio_pika import ExchangeType
from aio_pika.abc import AbstractRobustExchange, AbstractRobustQueue, AbstractRobustChannel

from sparta.rabbit.connection import RabbitMQConnectionProvider


class RabbitMQBaseClient(object):
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

    @staticmethod
    async def get_queue(
        channel: AbstractRobustChannel,
        queue_name: str,
        declare_if_missing=False,
        **kwargs,
    ):
        try:
            return await channel.get_queue(queue_name)
        except Exception as e:
            if not declare_if_missing:
                raise e
            return await channel.declare_queue(queue_name, **kwargs)

    @staticmethod
    async def get_exchange(
        channel: AbstractRobustChannel,
        exchange_name: str,
        declare_if_missing=False,
        **kwargs,
    ):
        try:
            return await channel.get_exchange(exchange_name)
        except Exception as e:
            if not declare_if_missing:
                raise e
            return await channel.declare_exchange(exchange_name, **kwargs)
