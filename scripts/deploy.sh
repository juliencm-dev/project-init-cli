#!/bin/bash

docker kill {{PROJECT_NAME}}
docker image rm -f "ghcr.io/$GIT_USERNAME/{{PROJECT_NAME}}:latest"
docker system prune -f
docker compose up -d 
