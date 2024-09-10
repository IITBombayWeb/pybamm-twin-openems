#!/bin/bash

# Fetch the latest openems-ui.zip URL
URL=$(curl -s https://api.github.com/repos/OpenEMS/openems/releases/latest | grep "browser_download_url.*openems-ui.zip" | cut -d '"' -f 4)

# Check if URL is fetched correctly
echo "Fetched URL: $URL"

# Exit if URL is not fetched
if [ -z "$URL" ]; then
  echo "Failed to fetch URL for openems-ui.zip"
  exit 1
fi

# Download the openems-ui.zip file
wget -q -O openems-ui.zip "$URL"

# Verify the download
if [ ! -f "openems-ui.zip" ]; then
  echo "Failed to download openems-ui.zip"
  exit 1
fi

# Remove the existing directory 'm' and create a new one
rm -rf m
mkdir m

# Unzip the downloaded file into the directory 'm'
unzip openems-ui.zip -d m
