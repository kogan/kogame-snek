#!/bin/bash
set -e

# kill any running containers
docker-compose kill
# clean up
docker-compose rm -fv

docker-compose build kogame
docker-compose run --rm kogame ./manage.py migrate

echo "Starting app server"
docker-compose up -d kogame

echo "Installing javascript dependencies"
npm install
echo "Building frontend assets"
npm run build

echo "Server is now running at http://localhost:8001/"
