import asyncio
import json
import os
import uuid
import aioamqp

from database import db
from models import Link

RABBITMQ_HOST = 'rabbit'
RABBITMQ_LOGIN = 'guest'
RABBITMQ_PASSWORD = 'guest'


async def send(body):
    transport, protocol = await aioamqp.connect(host=RABBITMQ_HOST,
                                                port=5672,
                                                login=RABBITMQ_LOGIN,
                                                password=RABBITMQ_PASSWORD)
    channel = await protocol.channel()

    await channel.queue_declare(queue_name='hello')

    await channel.basic_publish(
        payload=body,
        exchange_name='',
        routing_key='hello'
    )

    print(" [x] Sent link")
    await protocol.close()
    transport.close()

loop = asyncio.get_event_loop()
