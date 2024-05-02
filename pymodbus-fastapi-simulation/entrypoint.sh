#!/bin/bash

# Activate the virtual environment
# If poetry is set to create a virtualenv, you would source it here.
# Example: source $VIRTUAL_ENV/bin/activate

# Execute the main process
python -m pymodbus_fastapi_simulation.modbus_server
