#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import redis
import logging

logging.basicConfig(filename='/var/tmp/python.log', filemode='w', level=logging.DEBUG)


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
            logging.error(e)

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value):
        self._client = value

    def publish(self, key, value):
        client = self.client
        client.publish(key, value)
