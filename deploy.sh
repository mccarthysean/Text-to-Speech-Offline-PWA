#!/bin/bash

# Ensure that the script exits if any command fails
set -e

# display only the name of the current branch you're on
echo "Checking the current branch..."
git rev-parse --abbrev-ref HEAD

echo "Fetching the latest changes..."
git fetch

echo "Checking out the 'main' branch..."
git checkout main

echo "Pulling the latest changes..."
git pull


# Set variable names from .env file
export $(cat .env | grep -v "^#" | xargs)

# # Gitlab repo
# export CI_REGISTRY=registry.gitlab.com
# export CI_PROJECT_NAMESPACE=mccarthysean
# export CI_PROJECT_NAME=text-to-speech
# export IMAGE=$CI_REGISTRY/$CI_PROJECT_NAMESPACE/$CI_PROJECT_NAME

# To ensure we use BuildKit for faster, more efficient builds
export DOCKER_BUILDKIT=1
export BUILDKIT_INLINE_CACHE=1
export COMPOSE_DOCKER_CLI_BUILD=1

# Set environment variables for the build
export TEXT_TO_SPEECH_IMAGE_PROD_FINAL="mccarthysean/text_to_speech:latest"

# Build the Docker image
echo ""
echo "Building the Docker image..."
docker-compose -f docker-compose.build.prod.yml build

# Push the image to Docker Hub (optional, if using a private registry or CI/CD)
echo ""
echo "Pushing the Docker image to Docker Hub..."
docker push $TEXT_TO_SPEECH_IMAGE_PROD_FINAL

# Deploy the service to Docker Swarm
echo ""
echo "Deploying the service to Docker Swarm..."
docker stack deploy -c docker-compose.prod.yml text_to_speech

echo ""
echo "Deployment completed successfully!"
exit 0

