#!/bin/bash

sh docker_remove.sh

echo "Restarting Docker Compose..."

docker-compose up -d