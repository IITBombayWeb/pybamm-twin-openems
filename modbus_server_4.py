import random
import time
import asyncio
from pymodbus.server.async_io import ModbusTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from threading import Thread

# Function to update registers with random values and set specific values at two addresses
def update_registers(context, address_1, address_2):
    i = 0
    j = 1
    while True:
        # Randomly update the first 100 registers
        values = [random.randint(50, 100) for _ in range(100)]
        context[0].setValues(3, 0, values)

        # Set value at address_1
        specific_value_1 = [values[i % 100] * 100]
        context[0].setValues(3, address_1, specific_value_1)

        # Set value at address_2
        specific_value_2 = [values[j % 100] * 100]
        context[0].setValues(3, address_2, specific_value_2)

        print(f"Set value at address {address_1}: {specific_value_1}")
        print(f"Set value at address {address_2}: {specific_value_2}")

        time.sleep(2)  # Update every 2 seconds
        i = (i + 1) % 100
        j = (j + 1) % 100

# Set up the data store with enough registers
# Creating 1001 registers, so that address 1000 and beyond are valid
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0] * 1001),  # Discrete Inputs
    co=ModbusSequentialDataBlock(0, [0] * 1001),  # Coils
    hr=ModbusSequentialDataBlock(0, [0] * 1001),  # Holding Registers
    ir=ModbusSequentialDataBlock(0, [0] * 1001)   # Input Registers
)

context = ModbusServerContext(slaves=store, single=True)

# Set up device information
identity = ModbusDeviceIdentification()
identity.VendorName = 'pymodbus'
identity.ProductCode = 'PM'
identity.VendorUrl = 'https://github.com/riptideio/pymodbus'
identity.ProductName = 'pymodbus Server'
identity.ModelName = 'pymodbus Server'
identity.MajorMinorRevision = '1.0'

# Start a thread to update registers, with two different addresses
update_thread = Thread(target=update_registers, args=(context, 1000, 1001))  # Example: update address 1000 and 1001
update_thread.daemon = True
update_thread.start()

async def run_server():
    # Create and start Modbus TCP server on laptop's IP address:5020

    # server = socket.socket() 
    # server.bind(("10.64.1.49", 5020)) 
    # server.listen(4) 
    # client_socket, client_address = server.accept()
    server = ModbusTcpServer(context, identity=identity, address=("0.0.0.0", 5021))
    print(f"Starting Modbus server on localhost:5021")
    await server.serve_forever()

# Run the server within an event loop
if __name__ == "__main__":
    asyncio.run(run_server())
