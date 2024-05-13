#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

# Optionally: Pull the latest changes from the Git repository
echo "Updating repository..."
git pull origin main

# Navigate to the directory containing Dockerfiles if they're not in the root
# cd /path/to/your/project/directory

# Building Docker images
echo "Building openems-backend..."
cd openems-backend
./downloadBackend.sh
docker build -t openems-backend .

echo "Building openems-edge..."
cd ../openems-edge
./downloadEdge.sh
docker build -t openems-edge .

echo "Building openems-ui-backend..."
cd ../openems-ui
docker build -f backend.Dockerfile -t openems-ui-backend .

echo "Building openems-ui-edge..."
docker build -f edge.Dockerfile -t openems-ui-edge .

# Assuming docker-compose.yml is in the root or adjust path accordingly
cd ..

# Bring down the current containers and restart with new images
echo "Restarting services with new configurations..."
docker-compose down
docker-compose up -d --force-recreate

echo "Ensuring all containers are up and running..."
docker-compose ps

# Optional: Check if all services are running correctly
# Customize this based on your services
if docker-compose ps | grep -v "Up"; then
    echo "Some services are not running properly:"
    docker-compose ps
    exit 1
fi

echo "Deployment completed successfully."
