#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from pymongo import MongoClient
import requests
response = requests.get("http://vcd00.com")
print(response)

try:
    host = os.getenv('MONGO_INITDB_HOST', 'mongodb')  # This is the alias in Docker
    username = os.getenv('MONGO_INITDB_ROOT_USERNAME')
    password = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
    database = os.getenv('MONGO_INITDB_DATABASE')
    port = 27017
    client = MongoClient(
        host=[str(host) + ":" + str(port)],
        serverSelectionTimeoutMS=3000,  # 3 second timeout
        username=str(username),
        password=str(password)
    )
    google_database = client[database]
    res = google_database.place_info.find()
    for place_info in res:
        key = list(place_info.keys())[1]
        place_info_values = place_info.get(key)
        website = place_info_values.get('website', "")
        name = place_info_values.get('name', "")
        rating = place_info_values.get('rating', 0.0)
        international_phone_number = place_info_values.get('international_phone_number', "")
        formatted_address = place_info_values.get('formatted_address', "")
        place_id = place_info_values.get('place_id', "")



        break
except Exception as e:
    print(e)
