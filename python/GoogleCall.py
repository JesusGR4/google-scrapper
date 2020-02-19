#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from pymongo import MongoClient, errors
import os

port = 27017
host = os.getenv('MONGO_INITDB_HOST', 'mongodb') #This is the alias in Docker
username = os.getenv('MONGO_INITDB_ROOT_USERNAME')
password = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
database = os.getenv('MONGO_INITDB_DATABASE')
# use a try-except indentation to catch MongoClient() errors
try:
    # try to instantiate a client instance
    client = MongoClient(
        host = [ str(host) + ":" + str(port) ],
        serverSelectionTimeoutMS = 3000, # 3 second timeout
        username = str(username),
        password = str(password),
    )

    # print the version of MongoDB server if connection successful
    print ("server version:", client.server_info()["version"])

    # get the database_names from the MongoClient()
    database_names = client.list_database_names()

except errors.ServerSelectionTimeoutError as err:
    # set the client and DB name list to 'None' and `[]` if exception
    client = None
    database_names = []

    # catch pymongo.errors.ServerSelectionTimeoutError
    print ("pymongo ERROR:", err)

print ("\ndatabases:", database_names)
