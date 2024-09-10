import socket
from pymodbus.client import ModbusTcpClient
import time

# # Function to get the IP address of the host machine
# def get_host_ip():
#     hostname = socket.gethostname()
#     ip_address = socket.gethostbyname(hostname)
#     return ip_address

# # Get the host IP address
# host_ip = get_host_ip()
# print(f"Host IP Address: {host_ip}")

# Set up the client with the host IP address
client = ModbusTcpClient("10.2.161.46", port=5021)

# Connect to the Modbus server
if client.connect():
    print(f"Connected to Modbus server at localhost")

    try:
        while True:
            # Read holding registers at address 1000 and 1001
            response_1000 = client.read_holding_registers(1000, 1)
            response_1001 = client.read_holding_registers(1001, 1)
            
            if response_1000.isError():
                print(f"Error reading address 1000: {response_1000}")
            else:
                print(f"Value at address 1000: {response_1000.registers[0]}")
            
            if response_1001.isError():
                print(f"Error reading address 1001: {response_1001}")
            else:
                print(f"Value at address 1001: {response_1001.registers[0]}")

            # Wait for a second before the next read
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped by user")
    finally:
        client.close()
else:
    print(f"Failed to connect to Modbus server at ")
