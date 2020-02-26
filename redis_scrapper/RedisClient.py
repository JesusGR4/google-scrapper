#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import redis
from config import logger


class RedisClient(object):
    _redis_host = os.getenv('REDIS_HOST', 'localhost')
    _redis_password = os.getenv('REDIS_PASSWORD', 'localhost')
    _client = None

    def __init__(self):
        try:
            pool = redis.ConnectionPool(host=self._redis_host, port=6379, password=self._redis_password, db=0)
            r = redis.Redis(connection_pool=pool)
            self.client = r
        except Exception as e:
            logger.error(e)

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value):
        self._client = value

    def publish(self, key, value):
        client = self.client
        client.publish(key, value)

    def set(self, key, value):
        client = self.client
        client.set(key, value)

    def hmset(self, key, value):
        client = self.client
        client.hmset(key, value)

    def get(self, key):
        client = self.client
        return client.get(key)

    def hgetall(self, key):
        client = self.client
        return client.hgetall(key)