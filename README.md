# OpenEMS

https://openems.github.io/openems.io/openems/latest/gettingstarted.html

Running OpenEMS ecosystem in docker (with some simulation enabled)

# Docker

## Build

Enter the following commands in their respective folders.

```
cd openems-backend
./downloadBackend.sh
docker build -t openems-backend .
```

```
cd openems-edge
./downloadEdge.sh
docker build -t openems-edge .
```

```
cd openems-ui
docker build -f backend.Dockerfile -t openems-ui-backend .
docker build -f edge.Dockerfile -t openems-ui-edge .
```

## Run

`docker-compose up --force-recreate`

# OpenEMS Edge
## Apache Felix Web Console Configuration 
http://localhost:8080/system/console/configMgr

## UI
http://localhost:4201


# OpenEMS backend
## Apache Felix Web Console Configuration 
http://localhost:8079/system/console/configMgr

## UI
http://localhost:4202

### Useful links
Simulate OCPP connection:
https://simplesimulator.consolinno-it.de/

Simply point it at `ws://localhost:8887`

# Deployment Guide

This guide provides step-by-step instructions for setting up and deploying the CI/CD pipeline for your project using Docker and GitHub Actions.

## Prerequisites

1. **Ubuntu Server**: Ensure you have access to an Ubuntu server.
2. **GitHub Repository**: Ensure you have a GitHub repository set up for your project.

## Step 1: Install Docker and Docker Compose

Update the package list and install necessary packages:

```sh
sudo apt update
sudo apt upgrade -y
clear
sudo apt install -y ca-certificates curl gnupg lsb-release
```

Add Docker’s official GPG key and set up the stable repository:
  
```sh
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Update the package list and install Docker and Docker Compose:

```sh
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo docker run hello-world
```

Download and install the latest version of Docker Compose:

```sh
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

Install net-tools:

```sh
sudo apt install -y net-tools
```

## Step 2: Install Git

Install Git:

```sh
sudo apt install -y git
```

## Step 3: Set Up SSH Key

Generate a new SSH key:

```sh
ssh-keygen -t ed25519 -C "YOUR EMAIL ADDRESS"
```

Start the SSH agent and add your SSH key:

```sh
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

Add the SSH key to your GitHub account by copying the public key to your clipboard:

```sh
cat ~/.ssh/id_ed25519.pub
```

Verify your SSH key setup with GitHub:

```sh
ssh -T git@github.com
```

## Step 4: Clone the Repository and Deploy

Navigate to the applications directory:

```sh
cd /var/www/
mkdir applications
cd applications/
```

Clone your GitHub repository:

```sh
git clone git@github.com:ssingularitytech/openems_poc.git
cd openems_poc/
```

Deploy the backend:

```sh
sh deploy.backend.sh
```

If backend and edge are on the same server, also deploy the edge:
  
```sh
sh deploy.edge.sh
```