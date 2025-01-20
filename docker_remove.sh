#!/bin/bash

# Nom des services/containers/images à gérer
CONTAINERS=("octave_db" "octave_test-api-1" "octave_test-web-1")
IMAGES=("octave_test-api" "octave_test-web")
VOLUME="octave_db_data"
DOCKER_COMPOSE_FILE="docker-compose.yml"

echo "Stopping Docker Compose services..."
docker-compose down

echo "Removing specified containers..."
for container in "${CONTAINERS[@]}"; do
  if docker ps -a --format "{{.Names}}" | grep -q "^$container$"; then
    docker rm -f "$container"
    echo "Removed container: $container"
  # else
  #   echo "Container $container does not exist."
  fi
done

echo "Removing specified image..."
for image in "${IMAGES[@]}"; do
  if docker images --format "{{.Repository}}" | grep -q "^$image$"; then
    docker rmi "$image" --force
    echo "Removed image: $image"
  # else
  #   echo "Image $image does not exist."
  fi
done

echo "Removing specified volume..."
if docker volume ls --format "{{.Name}}" | grep -q "^$VOLUME$"; then
  docker volume rm "$VOLUME"
  echo "Removed volume: $VOLUME"
# else
#   echo "Volume $VOLUME does not exist."
fi

echo "Done, Docker Compose services have been stopped and removed."

