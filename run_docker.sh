#!/bin/sh

docker-compose up -d ticker-database
docker-compose build
docker-compose run flyway
docker-compose up -d ticker
