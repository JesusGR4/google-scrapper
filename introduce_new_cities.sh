#!/bin/bash

if [ -z "$1" ]; then
    echo "Error: Set a Query as first argument." >&2
    exit 1
fi

if [ -z "$2" ]; then
    echo "Error: Set a Location as second argument." >&2
    exit 1
fi

if [ -z "$1" ]; then
    echo "Error: Set a Type as third argument." >&2
    exit 1
fi

if [[ "$(docker images -q google-scrapper_publish-places:latest 2> /dev/null)" == "" ]]; then
  # Build image if it is necessary!
  docker build -t google-scrapper_publish-places .
fi

# Run docker and kill it
docker run --rm --network container:redis-container --env-file .env -v "$(pwd):/usr/src" google-scrapper_publish-places bash -c "python introduce_new_cities.py $1 $2 $3"
echo "Sent info!"