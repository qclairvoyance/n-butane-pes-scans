import os
import subprocess
import shutil
import matplotlib.pyplot as plt
import re

import subprocess
import os

# Define the directory where you want to open the Command Prompt
directory = r'<current-directory>'

# Define the command to run in the Command Prompt
command_to_run = 'rungms.bat butane_rotation_000.inp 2023.R1.intel 1 out_fuck'  

if os.path.exists(directory):
    subprocess.run(f'cmd.exe /K "cd {directory} && {command_to_run}"', shell=True)
else:
    print(f"The directory {directory} does not exist.")

for angle in range(0, 361, 10):
    print(f"butane_rotation_{str(angle).zfill(3)}.inp")
    directory = r'<input-file-directory>'
    command_to_run = f'rungms.bat butane_rotation_{str(angle).zfill(3)}.inp 2023.R1.intel 1 out_{str(angle).zfill(3)}'
    if os.path.exists(directory):
        subprocess.run(f'cmd.exe /K "cd {directory} && {command_to_run}"', shell=True)
    else:
        print(f"The directory {directory} does not exist.")

# Define the directory where the output files are located
output_dir = r'<outfit-file-directory>'  

# List all files in the directory (assuming they follow the naming pattern out_XXX.out)
output_files = [f for f in os.listdir(output_dir) if f.startswith('out_')]

# List to store extracted total energy values
total_energies = []

# Regular expression pattern to match the total energy line and extract the float value
energy_pattern = re.compile(r'TOTAL ENERGY =\s*(-?\d+\.\d+)')

# Loop through each file and extract the total energy value
for file_name in output_files:
    file_path = os.path.join(output_dir, file_name)

    try:
        # Open the output file and read through the lines
        with open(file_path, 'r') as file:
            for line in file:
                # Search for the line containing 'TOTAL ENERGY ='
                match = energy_pattern.search(line)
                if match:
                    # Extract the floating-point number and append it to the list
                    energy_value = float(match.group(1))  
                    total_energies.append(energy_value)
                    break  
    except Exception as e:
        print(f"Error reading file {file_name}: {e}")


plt.style.use('ggplot')
plt.figure(figsize = (7, 6), dpi = 300)
plt.plot(range(0, 361, 10), total_energies[:-1])
plt.xlabel('Angle in degrees')
plt.ylabel('Energy in Hartree')
plt.title('Butane Dihedral Scan')
plt.savefig('butane_plot.png')
