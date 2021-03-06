from django.core.management.base import BaseCommand
from pymongo import MongoClient
from place_info.models import PlaceInfo
import os
import logging
import requests


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            logger = logging.getLogger('stranger_sites_logger')
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
                if not place_info_values:
                    print(place_info)
                    logger.warning("No place info found")
                    continue
                place_id = place_info_values.get('place_id', None)
                if PlaceInfo.objects.filter(place_id=place_id).exists():
                    print(place_id)
                    continue
                website = place_info_values.get('website', None)
                name = place_info_values.get('name', None)
                rating = place_info_values.get('rating', 0.0)
                international_phone_number = place_info_values.get('international_phone_number', None)
                formatted_address = place_info_values.get('formatted_address', None)

                place_info_instance = PlaceInfo()
                place_info_instance.website = website
                place_info_instance.name = name
                place_info_instance.rating = rating
                place_info_instance.international_phone_number = international_phone_number
                place_info_instance.address = formatted_address
                place_info_instance.place_id = place_id
                if not website:
                    place_info_instance.web_status = "no_website"
                else:
                    try:
                        response = requests.get(website)
                        place_info_instance.web_status = response.status_code
                    except requests.exceptions.Timeout as e:
                        logger.warning('timeout')
                        print(e)
                        place_info_instance.web_status = "timeout"
                        # Maybe set up for a retry, or continue in a retry loop
                    except requests.exceptions.TooManyRedirects as e:
                        print(e)
                        logger.warning('too_many_redirects')
                        place_info_instance.web_status = "too_many_redirects"
                    except requests.exceptions.RequestException as e:
                        print(e)
                        logger.warning(e)
                        place_info_instance.web_status = "request_exception"
                place_info_instance.save()

        except Exception as e:
            logger.error(e)
            print(website)

