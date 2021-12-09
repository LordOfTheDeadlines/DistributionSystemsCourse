import asyncio
import aiohttp
import aioamqp
import redis
import requests

from models import Link
from database import db
from app import app
from app_redis import r

db.app = app

RABBITMQ_HOST = 'rabbit'
RABBITMQ_LOGIN = 'guest'
RABBITMQ_PASSWORD = 'guest'


async def callback(channel, body, envelope, properties):
    print(" [x] Received %r" % body)
    link = Link.query.get(int(body))
    url = link.link
    if r.exists(url):
        print('[x] Use redis')
        status = int(r.get(url))
    else:
        print('[x] Use session')
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as resp:
                    status = resp.status
            except:
                status = 404
            finally:
                r.set(url, str(status))

    link.status_code = status
    db.session.commit()
    print('[x] Callback end')


async def receive():
    transport, protocol = await aioamqp.connect(host=RABBITMQ_HOST,
                                                port=5672,
                                                login=RABBITMQ_LOGIN,
                                                password=RABBITMQ_PASSWORD)
    channel = await protocol.channel()

    await channel.queue_declare(queue_name='hello')

    await channel.basic_consume(callback, queue_name='hello')


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(receive())
event_loop.run_forever()
