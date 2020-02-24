#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from google.GoogleRequest import GoogleRequestPlaceTextSearch

if '__name__' == '__main__':
  object = GoogleRequestPlaceTextSearch(query="hotel", location="Sevilla", type="lodging")
  object.build_url()
  object.make_get_request()