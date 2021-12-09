import json
import os
import uuid

import redis

from flask import Flask, render_template, request, make_response, jsonify, url_for
from werkzeug.utils import secure_filename, redirect

from config import Configuration
#from modules.amqp import loop, send
from database import db
from views import links

app = Flask(__name__, static_folder="static")
app.config.from_object(Configuration)
app.register_blueprint(links, url_prefix='/links')
db.init_app(app)
db.app = app
db.create_all()

"""
Функция отправкии сообщений в очередь
"""


def sendMessageInRabbit(request, body):
    print(' [x] Send message to SDK')
    loop.run_until_complete(send(body, 'emoshape'))


"""
Вспомогательные функции
"""

def getRedisMessage(key=''):
    if 'DEBUG' in os.environ:
        r = redis.Redis(host='redis')
    else:
        r = redis.Redis()

    for item in r.scan_iter():
        if key in str(item):
            redisData = r.get(key)
            r.delete(key)
            return json.loads(redisData)
    return False


def sendRedisMessage(key, message):
    if 'DEBUG' in os.environ:
        r = redis.Redis(host='redis')
    else:
        r = redis.Redis()
    r.set(key, message)
