#!/bin/sh

sudo docker stop corere
sudo docker build -t corere .

(cd ./postgres/;./postgres.sh)

sudo docker run --name corere --network postgres-network -d -p 5000:5000 corere
