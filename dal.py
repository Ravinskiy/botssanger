# -*- coding: UTF-8 -*-
"""
Redis async client usage example
https://github.com/thefab/tornadis/blob/master/examples/web.py
"""

# import time
from itertools import chain
import tornadis
from tornado import gen
from settings import REDIS_HOST, REDIS_PORT, REDIS_POOL_SIZE
# from tornado.ioloop import IOLoop

# client = tornadis.Client(host="localhost", port=6379, autoconnect=True)
REDIS_POOL = tornadis.ClientPool(
    max_size=REDIS_POOL_SIZE,
    host=REDIS_HOST,
    port=REDIS_PORT,
    autoconnect=True
)


# @gen.coroutine
# def async_sleep(seconds=1):
#     yield gen.Task(IOLoop.instance().add_timeout, time.time() + seconds)


@gen.coroutine
def redis_ping() -> str:
    with (yield REDIS_POOL.connected_client()) as client:
        reply = yield client.call('PING')
        return str(reply, 'utf-8')


@gen.coroutine
def redis_set(key: str, val: str) -> str:
    with (yield REDIS_POOL.connected_client()) as client:
        reply = yield client.call('SET', key, val)
        return str(reply, 'utf-8')


@gen.coroutine
def redis_get(key: str) -> str:
    with (yield REDIS_POOL.connected_client()) as client:
        reply = yield client.call('GET', key)
        return str(reply, 'utf-8')


@gen.coroutine
def redis_mset(key_vals: dict) -> str:
    key_vals = tuple(chain.from_iterable(key_vals.items()))
    with (yield REDIS_POOL.connected_client()) as client:
        reply = yield client.call('MSET', *key_vals)
        return str(reply, 'utf-8')


@gen.coroutine
def redis_mget(keys: list) -> list:
    with (yield REDIS_POOL.connected_client()) as client:
        reply = yield client.call('MGET', *keys)
        return reply


@gen.coroutine
def redis_dict_set(dict_name: str, key: str, val: str) -> str:
    with (yield REDIS_POOL.connected_client()) as client:
        reply = yield client.call('HSET', dict_name, key, val)
        return str(reply, 'utf-8')


@gen.coroutine
def redis_dict_get(dict_name: str, key: str) -> str:
    with (yield REDIS_POOL.connected_client()) as client:
        reply = yield client.call('HGET', dict_name, key)
        return str(reply, 'utf-8')


@gen.coroutine
def redis_del(keys: list) -> int:
    with (yield REDIS_POOL.connected_client()) as client:
        reply = yield client.call('DEL', *keys)
        return reply


@gen.coroutine
def redis_exists(key: str) -> str:
    with (yield REDIS_POOL.connected_client()) as client:
        reply = yield client.call('EXISTS', key)
        return bool(reply)


# @gen.coroutine
# def test_func():
#     rp = yield redis_ping()
#     print(rp)
#     # rp = yield redis_mset({'bobr': 'dobr', 'kobr': 'hitr'})
#     # print(rp)
#     rp = yield redis_exists('bobr')
#     print(rp)


# test_func()

# # Start a tornado IOLoop, execute the coroutine and end the program
# loop = tornado.ioloop.IOLoop.instance()
# loop.run_sync(async_sleep)
