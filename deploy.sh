#!/bin/sh

# Build the images
docker build -t webstats_docker_nginx:latest -f nginx/Dockerfile nginx/
docker build -t xaratustrah/webstats_docker:latest -f webstats/Dockerfile webstats/

# Copy the public key to host
mkdir -p ~/.ssh
docker run xaratustrah/webstats_docker:latest cat /home/flask/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

# pass current user and set up the stack
DOCKERHOST_USER=$USER DOCKERHOST=172.18.0.1 docker stack deploy -c docker-compose_stack.yml webstats_docker_stack
