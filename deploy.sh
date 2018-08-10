#!/bin/sh
docker build -t webstats_docker_nginx:latest -f nginx/Dockerfile nginx/
docker build -t xaratustrah/webstats_docker:latest -f webstats/Dockerfile webstats/
docker stack deploy -c docker-compose_stack.yml webstats_docker_stack
