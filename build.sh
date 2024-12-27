#!/bin/bash

docker buildx build . -t "ghcr.io/$GIT_USERNAME/{{PROJECT_NAME}}:latest" --push
