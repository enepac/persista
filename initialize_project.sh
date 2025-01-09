#!/bin/bash

# Check if Docker is installed
if ! [ -x "$(command -v docker)" ]; then
  echo "Error: Docker is not installed." >&2
  exit 1
fi

# Check if Docker is running
if (! docker stats --no-stream ); then
  echo "Error: Docker is not running. Please start Docker and try again." >&2
  exit 1
fi

# Build and start Docker containers
echo "Building and starting Docker containers..."
docker-compose up -d --build

# Wait for services to become healthy
echo "Waiting for services to become healthy..."
sleep 10

# Check the health of all services
echo "Checking service health statuses..."
docker ps --filter "health=healthy"

# Ensure README.md exists in project-workspaces
PROJECT_WORKSPACES="./project-workspaces"
if [ ! -d "$PROJECT_WORKSPACES" ]; then
  echo "Error: Project workspaces directory does not exist." >&2
  exit 1
fi

if [ ! -f "$PROJECT_WORKSPACES/README.md" ]; then
  echo "Creating placeholder README.md in project-workspaces..."
  echo "# Project Workspaces" > "$PROJECT_WORKSPACES/README.md"
fi

echo "Initialization complete!"
