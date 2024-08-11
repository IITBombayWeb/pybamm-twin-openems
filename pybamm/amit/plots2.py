import pybamm
import numpy as np
import os
import liionpack as lp
import matplotlib.pyplot as plt

# Generate the netlist
netlist = lp.setup_circuit(Np=2, Ns=3, Rb=1e-4, Rc=1e-2, Ri=5e-2, V=1.5, I=80.0)

# Define the experiment
experiment = pybamm.Experiment(
    [
        "Discharge at 2.5 A for 240 minutes",
        "Rest for 15 minutes",
        "Charge at 2.5 A for 400 minutes",
        "Rest for 15 minutes",
    ],
    period="10 seconds",
)

# Define the parameter values and model
parameter_values = pybamm.ParameterValues("Chen2020")

# Define the output variables
output_variables = [
    "X-averaged negative particle surface concentration [mol.m-3]",
    "X-averaged positive particle surface concentration [mol.m-3]",
    "Terminal voltage [V]",
    "Current [A]",
    "Battery open-circuit voltage [V]",
]

InitialSoC = 1.0

# Solve the pack
output = lp.solve(
    netlist=netlist,
    parameter_values=parameter_values,
    experiment=experiment,
    output_variables=output_variables,
    initial_soc=InitialSoC
)

print(output)

# Extract data for manual SoC calculation
time = output["Time [s]"]
current = output["Current [A]"].mean(axis=1)  # Average current across cells

# Extract battery capacity from the parameter values
battery_capacity_Ah = parameter_values["Nominal cell capacity [A.h]"]

# Convert battery capacity to amp-seconds (As)
battery_capacity_As = battery_capacity_Ah * 3600

# Calculate cumulative charge in ampere-seconds (As)
cumulative_charge_As = np.cumsum(current * np.diff(np.insert(time, 0, 0)))

# Calculate SoC as a percentage
soc = (battery_capacity_As - cumulative_charge_As / battery_capacity_As) * 100 + InitialSoC * 100

# Ensure output directory exists
output_dir = 'output2'
os.makedirs(output_dir, exist_ok=True)

# Function to plot voltage and SoC
def plot_voltage_soc(output, soc, output_dir):
    time = output["Time [s]"]
    voltage = output["Terminal voltage [V]"]

    # Plot voltage and SoC vs time on the same graph
    fig, ax1 = plt.subplots()

    ax1.plot(time, voltage, 'b-', label='Voltage')
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Voltage [V]', color='b')
    ax1.tick_params(axis='y', labelcolor='b')

    ax2 = ax1.twinx()  # Instantiate a second y-axis that shares the same x-axis
    ax2.plot(time, soc, 'g-', label='State of Charge')
    ax2.set_ylabel('State of Charge (SOC) [%]', color='g')
    ax2.tick_params(axis='y', labelcolor='g')

    # Adding a title and legend
    fig.suptitle('Voltage and State of Charge vs Time')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'voltage_soc.png'))
    plt.close()

# Function to plot current and SoC
def plot_current_soc(output, soc, output_dir):
    time = output["Time [s]"]
    current = output["Current [A]"].mean(axis=1)  # Average current across cells

    # Plot current and SoC vs time on the same graph
    fig, ax1 = plt.subplots()

    ax1.plot(time, current, 'r-', label='Current')
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Current [A]', color='r')
    ax1.tick_params(axis='y', labelcolor='r')

    ax2 = ax1.twinx()  # Instantiate a second y-axis that shares the same x-axis
    ax2.plot(time, soc, 'g-', label='State of Charge')
    ax2.set_ylabel('State of Charge (SOC) [%]', color='g')
    ax2.tick_params(axis='y', labelcolor='g')

    # Adding a title and legend
    fig.suptitle('Current and State of Charge vs Time')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'current_soc.png'))
    plt.close()

# Plot the standard output, voltage/SoC graph, and current/SoC graph
lp.plot_output(output)
plt.savefig(os.path.join(output_dir, 'standard_output.png'))
plt.close()

plot_voltage_soc(output, soc, output_dir)
plot_current_soc(output, soc, output_dir)
