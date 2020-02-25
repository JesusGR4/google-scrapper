#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from google.GoogleRequest import GoogleRequestPlaceTextSearch
from redis_scrapper.RedisClient import RedisClient

try:
    redis = RedisClient()
    redis_client = redis.client
    values = redis_client.get('place_id_*')
    print(values)

except Exception as e:
    print(e)
