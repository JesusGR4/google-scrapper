#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from redis_scrapper.RedisClient import RedisClient
import sys, json

args = sys.argv

if len(args) != 4:
    print("You must write query, location and type :D")
    exit(1)

query = args[1]
location = args[2]
type = args[3]
redis = RedisClient()

redis.publish('city', json.dumps({'query': query,
                                 'location': location,
                                 'type': type}))
