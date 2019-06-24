docker system prune -f
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker build -t corere .
docker run -d -p 5000:5000 corere
