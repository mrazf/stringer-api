docker login -u=$DOCKER_USERNAME -p=$DOCKER_PASSWORD
docker build . -t mrazf/stringer-api:latest
docker push mrazf/stringer-api:latest