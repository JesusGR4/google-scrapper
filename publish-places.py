#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from google.GoogleRequest import GoogleRequestPlaceTextSearch
args = sys.argv

if len(args) != 4:
    print("You must write query, location and type :D")
    exit(1)

query = args[1]
location = args[2]
type = args[3]

try:
    request_place_search = GoogleRequestPlaceTextSearch(query=query, location=location, type=type)
    request_place_search.build_url()
    request_place_search.make_get_request()
except Exception as e:
    print(e)