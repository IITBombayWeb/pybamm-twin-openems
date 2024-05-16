#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

# Navigate to the directory containing Dockerfiles if they're not in the root
cd /var/www/applications/openems_poc

# Optionally: Pull the latest changes from the Git repository
echo "Updating repository..."
git pull origin main


# Building Docker images
echo "Building openems-edge..."
cd openems-edge
./downloadEdge.sh
docker build -t openems-edge .

echo "Building openems-ui-edge..."
cd ../openems-ui
docker build -f edge.Dockerfile -t openems-ui-edge .

# Assuming docker-compose.yml is in the root or adjust path accordingly
cd ..

# Bring down the current containers and restart with new images
echo "Restarting edge services with new configurations..."
docker-compose -f docker-compose.openems-edge.yml down
docker-compose -f docker-compose.openems-edge.yml up -d --force-recreate

echo "Ensuring all edge containers are up and running..."
docker-compose -f docker-compose.openems-edge.yml ps

# Optional: Check if all services are running correctly
# Customize this based on your services
if docker-compose -f docker-compose.openems-edge.yml ps | grep -v "Up"; then
    echo "Some edge services are not running properly:"
    docker-compose -f docker-compose.openems-edge.yml ps
    exit 1
fi

echo "Edge deployment completed successfully."
