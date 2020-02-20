#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymongo import MongoClient, errors
import os

class MongoConnection(object):
    _client = None
    _port = 27017
    _host = os.getenv('MONGO_INITDB_HOST', 'mongodb')  # This is the alias in Docker
    _username = os.getenv('MONGO_INITDB_ROOT_USERNAME')
    _password = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
    _database = os.getenv('MONGO_INITDB_DATABASE')

    def __init__(self):
        try:
            self.client = MongoClient(
                host=[str(self._host) + ":" + str(self._port)],
                serverSelectionTimeoutMS=3000,  # 3 second timeout
                username=str(self._username),
                password=str(self._password)
            )
        except errors.ServerSelectionTimeoutError as err:
            print("pymongo ERROR:", err)

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value):
        self._client = value


