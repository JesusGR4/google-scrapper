#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from google.GoogleRequest import GoogleRequestPlaceDetail
from redis_scrapper.RedisClient import RedisClient
import time, os
from config import logger

redis = RedisClient()
client = redis.client
redis_pubsub = client.pubsub()
redis_pubsub.subscribe('places_id')
timing = int(os.getenv('PLACES_ID_TIMING', 1))
while True:
    message = redis_pubsub.get_message()
    if message is not None:
        place_id = message['data']
        if(place_id == 1):
            continue
        decoded_place_id = place_id.decode("utf-8")
        logger.info('Importing the place_id -> %s', decoded_place_id)
        place_details = GoogleRequestPlaceDetail(decoded_place_id)
        place_details.build_url()
        json_response = place_details.make_get_request()
        place_details.insert_info_in_mongo(decoded_place_id, json_response)

    logger.info("Let's sleep waiting for info")
    time.sleep(timing)
