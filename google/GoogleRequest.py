#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import requests

from config import logger
from mongodb.MongoClient import MongoConnection
from redis_scrapper.RedisClient import RedisClient


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

    def make_get_request(self):
        raise NotImplementedError("You must define make get request")



class GoogleRequestPlaceTextSearch(GoogleRequest):
    _query = ""
    _location = ""
    _type = ""
    _next_token = None

    def __init__(self, query, location, type, next_token=None):
        self.api_uri = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
        self.query = query
        self.location = location
        self.type = type
        self.next_token = next_token

    @property
    def next_token(self):
        return self._next_token

    @next_token.setter
    def next_token(self, value):
        self._next_token = value

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
        url = self.api_uri + "query=" + self.query + "&location=" + self.location + "&type=" + self.type + "&key=" + self.google_key
        if self.next_token:
            url += "&nexttoken=" + self.next_token
        self.url = url

    def make_get_request(self):

        response = requests.get(self.url)
        json_response = response.json()
        return json_response

    def publish_place_id(self, place_id):
        redis = RedisClient()
        redis.publish('places_id', place_id)

class GoogleRequestPlaceDetail(GoogleRequest):
    _placeid = ""

    def __init__(self, placeid):
        self.api_uri = "https://maps.googleapis.com/maps/api/place/details/json?"
        self.placeid = placeid

    @property
    def placeid(self):
        return self._placeid

    @placeid.setter
    def placeid(self, value):
        self._placeid = value

    def build_url(self):
        self.url = self.api_uri + "placeid=" + str(self.placeid) + "&key=" + self.google_key

    def make_get_request(self):
        try:
            response = requests.get(self.url)
            json_response = response.json()
            place_info = json_response.get('result', {})
            if not place_info:
                logger.error('No place info fkn noob')
            return place_info

        except Exception as e:
            logger.error(e)

    def insert_info_in_mongo(self, place_id, place_info):
        mongo_object = MongoConnection()
        client = mongo_object.client
        database = mongo_object.database
        google_database = client[database]
        google_database.place_info.insert({place_id: place_info})