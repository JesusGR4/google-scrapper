#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from google.GoogleRequest import GoogleRequestPlaceDetail
from redis_scrapper.RedisClient import RedisClient
import time
import logging
logging.basicConfig(filename='/var/tmp/python.log', filemode='w', level=logging.DEBUG)

redis = RedisClient()
client = redis.client
redis_pubsub = client.pubsub()
redis_pubsub.subscribe('places_id')

while True:
    message = redis_pubsub.get_message()
    if message is not None:
        place_id = message['data']
        if(place_id == 1):
            continue
        decoded_place_id = place_id.decode("utf-8")
        logging.info('Importing the place_id -> %s', decoded_place_id)
        place_details = GoogleRequestPlaceDetail(decoded_place_id)
        place_details.build_url()
        place_details.make_get_request()
    logging.info("Let's sleep waiting for info")
    time.sleep(5)
