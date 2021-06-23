#!/bin/bash
echo "Tagging and pushing docker image. Be sure to start docker.app first"
echo "To examine contents: 'docker run -it {image} sh'"

docker rmi kineticsquid/calendar:latest
docker build --rm --no-cache --pull -t kineticsquid/calendar:latest -f Dockerfile .
docker push kineticsquid/calendar:latest

# list the current images
echo "Docker Images..."
docker images
