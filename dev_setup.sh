#!/bin/bash
set -e

# kill any running containers
docker-compose kill
# clean up
docker-compose rm -fv

docker-compose run --rm django ./manage.py migrate

echo "Please create a super user."
docker-compose run --rm django ./manage.py createsuperuser

echo "Starting webserver"
docker-compose up -d django

echo "Installing javascript dependencies"
npm install
echo "Building frontend assets"
npm run build

echo "Server is now running at http://localhost:8001/"
