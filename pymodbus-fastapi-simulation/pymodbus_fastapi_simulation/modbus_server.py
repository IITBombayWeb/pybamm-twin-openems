import asyncio
import logging
import random

from pymodbus.datastore import ModbusSequentialDataBlock, ModbusServerContext, ModbusSlaveContext
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server import StartAsyncTcpServer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_data_blocks():
    # Set up your data blocks here
    block = ModbusSequentialDataBlock(0x00, [0]*40)
    block.setValues(0, [50]*10)   # Example: Battery Charge Level
    block.setValues(10, [20]*10)  # Example: Solar Power Output
    block.setValues(20, [5]*10)   # Example: Grid Power
    block.setValues(30, [15]*10)  # Example: Consumption
    return block

async def update_data_blocks(block):
    while True:
        # Update data values here, example:
        block.setValues(10, [random.randint(10, 30)])  # Solar power output between 10kW to 30kW
        block.setValues(30, [random.randint(10, 20)])  # Consumption between 10kW to 20kW
        await asyncio.sleep(50)  # update every 50 seconds

async def run_modbus_server():
    try:
        block = setup_data_blocks()
        store = ModbusSlaveContext(hr=block)
        context = ModbusServerContext(slaves={0x01: store}, single=True)

        identity = ModbusDeviceIdentification()
        identity.VendorName = 'Pymodbus'
        identity.ProductCode = 'EMS-Sim'
        identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
        identity.ProductName = 'Electrical Management System Simulator'
        identity.ModelName = 'EMS Simulation'
        identity.MajorMinorRevision = '1.0'

        update_task = asyncio.create_task(update_data_blocks(block))  # Create a task for the updating coroutine
        logger.info("Starting Modbus TCP server for electrical management system simulation...")

        # Run the server as a coroutine
        await StartAsyncTcpServer(context=context, identity=identity, address=("localhost", 5020))
    except Exception as e:
        logger.error("Failed to start Modbus TCP server", exc_info=True)

def main():
    asyncio.run(run_modbus_server())

if __name__ == "__main__":
    main()
