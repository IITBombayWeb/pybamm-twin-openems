# Use a base image with Python
FROM python:3.10-slim

# Set the working directory
WORKDIR ./

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the Modbus server will use
EXPOSE 5020

# Command to run the Modbus server
CMD ["python", "modbus_server_4.py"]