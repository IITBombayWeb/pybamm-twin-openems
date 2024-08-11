from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.device import ModbusDeviceIdentification
import time
from threading import Thread

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Set up the Modbus datastore
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0]*100),
    co=ModbusSequentialDataBlock(0, [0]*100),
    hr=ModbusSequentialDataBlock(0, [0]*2000),  # Increased size for address 1000
    ir=ModbusSequentialDataBlock(0, [0]*100)
)
context = ModbusServerContext(slaves=store, single=True)

# Thread to update the register with a constant value
def updating_thread(context):
    while True:
        value = 100
        context[0].setValues(3, 1000, [value])  # Update holding register at address 1000 with value 100
        log.debug(f"Updated holding register at address 1000 with value: {value}")
        print(f"Updated holding register at address 1000 with value: {value}")
        time.sleep(1)

# Modbus device identification setup
identity = ModbusDeviceIdentification()
identity.VendorName = 'pymodbus'
identity.ProductCode = 'PM'
identity.VendorUrl = 'http://github.com/bashwork/pymodbus/'
identity.ProductName = 'pymodbus Server'
identity.ModelName = 'pymodbus Server'
identity.MajorMinorRevision = '1.0'

# Start the updating thread
thread = Thread(target=updating_thread, args=(context,))
thread.daemon = True
thread.start()

# Start the Modbus TCP server on port 8502
StartTcpServer(context=context, identity=identity, address=("localhost", 8502))
