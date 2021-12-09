import os

HOST = '0.0.0.0'
PORT = 5000
if 'DEBUG' in os.environ:
    HOST = os.environ.get('WEB_IP')
    PORT = os.environ.get('WEB_PORT')


class Configuration:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://hello_flask:hello_flask@db:5432/hello_flask_dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = os.environ['CACHE_TYPE']
    CACHE_REDIS_HOST = os.environ['CACHE_REDIS_HOST']
    CACHE_REDIS_PORT = os.environ['CACHE_REDIS_PORT']
    CACHE_REDIS_DB = os.environ['CACHE_REDIS_DB']
    CACHE_REDIS_URL = os.environ['CACHE_REDIS_URL']
    CACHE_DEFAULT_TIMEOUT = os.environ['CACHE_DEFAULT_TIMEOUT']