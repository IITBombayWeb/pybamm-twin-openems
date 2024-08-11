import pybamm
import numpy as np
import matplotlib.pyplot as plt
import os

# Define the model
model = pybamm.lithium_ion.SPMe()

# Load parameter values
parameter_values = pybamm.ParameterValues("Chen2020")
print(parameter_values)

# Set up the experiment
experiment = pybamm.Experiment(
    [
        "Charge at .001 A for 60000 minutes",
        "Rest for 1.5 minutes",
        "Discharge at 1 A until 4.0 V",
        "Rest for 1.5 minutes",
    ],
    period="10 seconds",
)

# Set initial state of charge
initial_soc = 0.5

# Define output variables
output_variables = [
    "X-averaged negative particle surface concentration",
    "X-averaged positive particle surface concentration",
    "Terminal voltage [V]",  # Use the dimensional version
    "Current [A]",
    "Discharge capacity [A.h]",
    
]

# Solve the model
sim = pybamm.Simulation(
    model,
    parameter_values=parameter_values,
    experiment=experiment,
    output_variables=output_variables,
)
sim.solve()

# Extract data
solution = sim.solution
time = solution["Time [s]"].data
current = solution["Current [A]"].data.squeeze()  # Ensure to remove unnecessary dimensions
min = solution
# Calculate integral of I*dt in A.h
integral_of_current = np.cumsum(current * np.diff(np.insert(time, 0, 0))) / 3600  # Convert from As to Ah

discharge_capacity = solution["Discharge capacity [A.h]"].data
# Calculate State of Charge (SoC)
battery_capacity_Ah = parameter_values["Nominal cell capacity [A.h]"]
battery_capacity_As = battery_capacity_Ah * 3600
soc = initial_soc * 100 - (np.cumsum(current * np.diff(np.insert(time, 0, 0))) / battery_capacity_As * 100)

# Ensure output directory exists
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

# Plotting functions
def plot_raw_current(time, current):
    plt.figure(figsize=(12, 8))
    plt.plot(time, current, label="Current [A]")
    plt.xlabel("Time [s]")
    plt.ylabel("Current [A]")
    plt.title("Raw Current vs Time")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'raw_current.png'))
    plt.close()

def plot_voltage_soc(time, voltage, soc):
    fig, ax1 = plt.subplots()

    ax1.plot(time, voltage, 'b-', label='Voltage')
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Voltage [V]', color='b')
    ax1.tick_params(axis='y', labelcolor='b')

    ax2 = ax1.twinx()  # Instantiate a second y-axis that shares the same x-axis
    ax2.plot(time, soc, 'g-', label='State of Charge')
    ax2.set_ylabel('State of Charge (SOC) [%]', color='g')
    ax2.tick_params(axis='y', labelcolor='g')

    fig.suptitle('Voltage and State of Charge vs Time')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'voltage_soc.png'))
    plt.close()

def plot_current_soc(time, current, soc):
    fig, ax1 = plt.subplots()

    ax1.plot(time, current, 'r-', label='Current')
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Current [A]', color='r')
    ax1.tick_params(axis='y', labelcolor='r')

    ax2 = ax1.twinx()  # Instantiate a second y-axis that shares the same x-axis
    ax2.plot(time, soc, 'g-', label='State of Charge')
    ax2.set_ylabel('State of Charge (SOC) [%]', color='g')
    ax2.tick_params(axis='y', labelcolor='g')

    fig.suptitle('Current and State of Charge vs Time')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'current_soc.png'))
    plt.close()

def plot_discharge_capacity_and_integral(time, discharge_capacity, integral):
    plt.figure(figsize=(12, 8))
    plt.plot(time, discharge_capacity, label="Discharge Capacity [A.h]")
    plt.plot(time, integral, label="Integral of I*dt [A.h]", linestyle='--')
    plt.xlabel("Time [s]")
    plt.ylabel("Capacity [A.h]")
    plt.title("Discharge Capacity and Integral of I*dt vs Time")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'discharge_capacity_and_integral.png'))
    plt.close()

# Generate plots
plot_raw_current(time, current)
plot_voltage_soc(time, solution["Terminal voltage [V]"].data, soc)  # Use dimensional version here
plot_current_soc(time, current, soc)
plot_discharge_capacity_and_integral(time, discharge_capacity, integral_of_current)
