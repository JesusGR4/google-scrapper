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


connection = MongoConnection()
mongo_client = connection.client


class GoogleRequest(object):
    _api_uri = ""
    _url = ""
    _google_key = os.getenv('GOOGLE_KEY', '')

    @property
    def api_uri(self):
        return self._api_uri

    @api_uri.setter
    def api_uri(self, value):
        self._api_uri = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def google_key(self):
        return self._google_key

    @google_key.setter
    def google_key(self, value):
        self._google_key = value

    def build_url(self):
        raise NotImplementedError("You must build an URL!")

    def make_request(self):
        pass


class GoogleRequestPlaceTextSearch(GoogleRequest):
    _query = ""
    _location = ""
    _type = ""

    def __init__(self, query, location, type):
        self.api_uri = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
        self.query = query
        self.location = location
        self.type = type

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value):
        self._query = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    def build_url(self):
        self.url = self.api_uri + "query=" + self.query + "&location=" + self.location + "&type=" + self.type + "&key=" + self.google_key


class GoogleRequestPlaceDetail(GoogleRequest):
    _placeid = ""

    def __init__(self, placeid):
        self.api_uri = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
        self.placeid = placeid

    @property
    def placeid(self):
        return self._placeid

    @placeid.setter
    def placeid(self, value):
        self._placeid = value

    def build_url(self):
        self.url = self.api_uri + "placeid=" + self.placeid + "&key=" + self.google_key

google_request_place_text_search = GoogleRequestPlaceTextSearch("hotel", "Sevilla", "type")
google_request_place_text_search.build_url()
print(google_request_place_text_search.url)