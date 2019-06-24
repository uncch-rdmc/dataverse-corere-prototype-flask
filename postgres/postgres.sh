#!/bin/bash

docker system prune -f
docker network prune -f
sudo docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker network rm postgres-network

sudo docker build -t postgresondocker:9.3 .
sudo docker network create --driver bridge postgres-network
sudo docker volume create pgdata

sudo docker run --name postgresondocker --network postgres-network -v pgdata:/var/lib/postgresql/9.3/main -p 5432:5432 -d postgresondocker:9.3
