#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

# Navigate to the directory containing Dockerfiles if they're not in the root
cd /var/www/applications/openems_poc

# Optionally: Pull the latest changes from the Git repository
echo "Updating repository..."
git pull origin main

# Building Docker images
echo "Building openems-backend..."
cd openems-backend
./downloadBackend.sh
docker build -t openems-backend .

echo "Building openems-ui-backend..."
cd ../openems-ui
docker build -f backend.Dockerfile -t openems-ui-backend .

# Backing up InfluxDB data
echo "Backing up InfluxDB data..."
docker exec openems-influxdb influx backup /var/lib/influxdb2/backup

# Assuming docker-compose.yml is in the root or adjust path accordingly
cd ..

# Bring down the current containers and restart with new images
echo "Restarting backend services with new configurations..."
docker-compose -f docker-compose.openems-backend.yml down
docker-compose -f docker-compose.openems-backend.yml up -d --force-recreate

echo "Ensuring all backend containers are up and running..."
docker-compose -f docker-compose.openems-backend.yml ps

# Optional: Check if all services are running correctly
# Customize this based on your services
if docker-compose -f docker-compose.openems-backend.yml ps | grep -v "Up"; then
    echo "Some backend services are not running properly:"
    docker-compose -f docker-compose.openems-backend.yml ps
    exit 1
fi

echo "Backend deployment completed successfully."
