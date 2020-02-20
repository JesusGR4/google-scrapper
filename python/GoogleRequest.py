#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import requests


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
    _next_token = ""

    def __init__(self, query, location, type, next_token=""):
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
