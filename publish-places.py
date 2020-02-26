#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from config import logger
from google.GoogleRequest import GoogleRequestPlaceTextSearch
import time, os, json

from redis_scrapper.RedisClient import RedisClient

timing = int(os.getenv('TEXT_SEARCH_TIMING', 1))
redis = RedisClient()
redis_pubsub = redis.client.pubsub()
redis_pubsub.subscribe('city')

while True:
    message = redis_pubsub.get_message()
    if message is not None:
        city_info = message['data']
        if (city_info == 1):
            continue
        try:
            city_info = json.loads(city_info)
            query = city_info.get('query')
            location = city_info.get('location')
            type = city_info.get('type')

            next_token = None
            redis_key = '%s_%s_%s' % (query, location, type)
            cached_values = redis.hgetall(redis_key)

            if cached_values:
                query = cached_values.get('query')
                location = cached_values.get('location')
                type = cached_values.get('type')
                next_token = cached_values.get('next_token')

            while (True):
                request_place_search = GoogleRequestPlaceTextSearch(query=query, location=location, type=type,
                                                                    next_token=next_token)

                request_place_search.build_url()
                json_response = request_place_search.make_get_request()
                next_token = json_response.get('next_page_token', None)
                results = json_response.get('results', [])

                for result in results:
                    place_id = result.get('place_id')
                    request_place_search.publish_place_id(place_id=place_id)

                redis.hmset(redis_key, {'query': query,
                                        'location': location,
                                        'type': type,
                                        'next_token': next_token})

                if not next_token:
                    break
                time.sleep(timing)
        except Exception as e:
            logger.error(e)
    logger.info("Let's sleep for a new city")
    time.sleep(timing)
