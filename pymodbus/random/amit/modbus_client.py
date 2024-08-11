from pymodbus.client import ModbusTcpClient


host = 'localhost'  
port = 8502
unit_id = 1


addresses = [1000, 1000]


client = ModbusTcpClient(host, port)

try:
    # while True:
        if client.connect():
            print(f"Connected to Modbus server at {host}:{port}")

            for address in addresses:
                response = client.read_holding_registers(address, 3, unit=unit_id)
                if not response.isError():
                    value = response.registers[0]
                    print(f"Value at register {address}: {value}")
                else:
                    print(f"Error reading register {address}: {response}")

            client.close()

        else:
            print(f"Failed to connect to Modbus server at {host}:{port}")

except Exception as e:
    print(f"An error occurred: {e}")
