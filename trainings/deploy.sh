#!/bin/bash

# Stop and remove existing containers, networks defined in the compose file
echo "Stopping and removing existing containers..."
docker compose down

# Build images (if Dockerfiles changed) and start services in detached mode
echo "Building images and starting containers..."
docker compose up --build -d

echo "Deployment complete!"
echo "Access JupyterLab at: http://localhost:8888"

