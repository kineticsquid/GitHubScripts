#!/bin/bash
echo "Tagging and pushing docker image. Be sure to start docker.app first"
echo "To examine contents: 'docker run -it {image} sh'"

docker rmi kineticsquid/test:latest
docker build --rm --no-cache --pull -t kineticsquid/test:latest -f Dockerfile .
docker push kineticsquid/test:latest

# list the current images
echo "Docker Images..."
docker images
