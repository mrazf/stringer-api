#!/usr/bin/env bash

docker-compose pull
docker-compose --verbose -f docker-compose-production.yml up