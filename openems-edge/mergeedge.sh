#!/bin/bash

# Unzip the downloaded JAR file into a directory
unzip openems-edge.jar -d openems-edge

# Copy your additional files into the jar directory
cp -r ./local/* openems-edge/jar/

# # Remove the original JAR file
rm openems-edge.jar

# # # Navigate into the directory where the files are
cd openems-edge

# # # Create a new JAR file with the added files and specify the manifest file
jar cfm ../openems-edge.jar ./META-INF/MANIFEST.MF start start.bat

# # # Navigate back to the original directory if needed
cd ..
