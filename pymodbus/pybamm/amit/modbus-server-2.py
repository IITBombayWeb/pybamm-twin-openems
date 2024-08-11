import random
import time
import asyncio
from pymodbus.server.async_io import ModbusTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from threading import Thread
import pybamm
import numpy as np
import liionpack as lp

# Define Pybamm setup
def mySPMEsim(parameter_values=None):
    # Create the pybamm model
    model = pybamm.lithium_ion.SPM()

    # Add events to the model
    model = lp.add_events_to_model(model)

    # Set up parameter values
    if parameter_values is None:
        param = pybamm.ParameterValues("Chen2020")
    else:
        param = parameter_values.copy()

    # Set up solver and simulation
    solver = pybamm.CasadiSolver(mode="safe")
    sim = pybamm.Simulation(
        model=model,
        parameter_values=param,
        solver=solver,
    )
    return sim

# Generate the netlist
netlist = lp.setup_circuit(Np=2, Ns=3, Rb=1e-4, Rc=1e-2, Ri=5e-2, V=1.5, I=80.0)

# Define the parameter values
parameter_values = pybamm.ParameterValues("Chen2020")

# Define the experiment
experiment = pybamm.Experiment(
    [
        "Discharge at 2.5 A for 240 minutes",
        "Rest for 15 minutes",
        "Charge at 1 A for 600 minutes",
        "Charge at 100 mA for 100 minutes",
        "Rest for 15 minutes",
    ],
    period="10 seconds",
)

# Start with a minimal set of output variables
output_variables = [
    "Terminal voltage [V]",
    "Current [A]",
    "X-averaged cell temperature [K]",
    "X-averaged cell temperature [C]",
]

# Update registers function with Pybamm data
def update_registers(context):
    InitialSoC = 1.0
    
    while True:
        # Run Pybamm simulation
        sim_output = lp.solve(
            netlist=netlist,
            parameter_values=parameter_values,
            experiment=experiment,
            sim_func=mySPMEsim,
            output_variables=output_variables,
            initial_soc=InitialSoC
        )

        # Extract data from Pybamm simulation
        sim_time = sim_output["Time [s]"]
        voltage = sim_output["Terminal voltage [V]"]
        current = sim_output["Current [A]"].mean(axis=1)  # Average current across cells
        
        # Extract battery capacity from the parameter values
        battery_capacity_Ah = parameter_values["Nominal cell capacity [A.h]"]
        battery_capacity_As = battery_capacity_Ah * 3600

        # Initialize cumulative charge and initial SoC
        cumulative_charge_As = 0
        initial_soc_as = InitialSoC * battery_capacity_As

        for i in range(len(sim_time)):
            if i > 0:
                # Calculate cumulative charge in ampere-seconds (As)
                cumulative_charge_As += current[i-1] * (sim_time[i] - sim_time[i-1])
            
            # Calculate SoC as a percentage
            soc = (initial_soc_as - cumulative_charge_As) / battery_capacity_As * 100
            
            # Extract the current voltage
            voltage_last = float(voltage[i][0])
            current_last = float(current[i])
            soc_last = float(soc)
            
            # Convert data to Modbus register format
            values = [
                int(voltage_last * 100),  
                int(current_last * 100),
                int(soc_last * 100),     
            ]
            
            # # Update Modbus registers
            # context[0].setValues(3, 1001, [values[0]])
            # print(f"Set voltage value at address 1001: {values[0]}")
            # context[0].setValues(3, 1002, [values[1]])
            # print(f"Set current value at address 1002: {values[1]}")
            # context[0].setValues(3, 1003, [values[2]])
            # print(f"Set SoC value at address 1003: {values[2]}")
            
            if i % 10 == 0:  
                # Update Modbus registers
                context[0].setValues(3, 1001, [values[0]])
                print(f"Set voltage value at address 1001: {values[0]}")
                context[0].setValues(3, 1002, [values[1]])
                print(f"Set current value at address 1002: {values[1]}")
                context[0].setValues(3, 1003, [values[2]])
                print(f"Set SoC value at address 1003: {values[2]}")

            time.sleep(1)  # Sleep for 1 second before updating again

# Modbus setup
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0]*2001),  # Discrete Inputs
    co=ModbusSequentialDataBlock(0, [0]*2001),  # Coils
    hr=ModbusSequentialDataBlock(0, [0]*2001),  # Holding Registers
    ir=ModbusSequentialDataBlock(0, [0]*2001)   # Input Registers
)

context = ModbusServerContext(slaves=store, single=True)

# Device information
identity = ModbusDeviceIdentification()
identity.VendorName = 'pymodbus'
identity.ProductCode = 'PM'
identity.VendorUrl = 'https://github.com/riptideio/pymodbus'
identity.ProductName = 'pymodbus Server'
identity.ModelName = 'pymodbus Server'
identity.MajorMinorRevision = '1.0'

# Start thread to update registers
update_thread = Thread(target=update_registers, args=(context,))
update_thread.daemon = True
update_thread.start()

# Async function to run Modbus server
async def run_server():
    server = ModbusTcpServer(context, identity=identity, address=("localhost", 5020))
    print("Starting Modbus server on localhost:5020")
    await server.serve_forever()

# Main entry point
if __name__ == "__main__":
    asyncio.run(run_server())
