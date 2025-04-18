import psi4
import glob
import os
import plotly.graph_objects as go
import plotly.io as pio

dihedral_angles = list(range(0,361,10))

# Define the n-butane molecule using internal coordinates
butane_internal = """
C
H   1 1.070
H   1 1.070  2 109.471
H   1 1.070  2 109.471  3 240.0
C   1 1.540  2 109.471  3 120.0
H   5 1.070  1 109.471  2  60.0
H   5 1.070  1 109.471  2 180.0
C   5 1.540  1 109.471  2 300.0
H   8 1.070  5 109.471  1 C8H9
H   8 1.070  5 109.471  1 C8H10
C   8 1.540  5 109.471  1 DHC11
H  11 1.070  8 109.471  5 180.0
H  11 1.070  8 109.471  5 300.0
H  11 1.070  8 109.471  5  60.0
"""

# Define the molecule in Psi4
molecule = psi4.geometry(butane_internal)

energy = []
i = 0
for DA in dihedral_angles:
    # calculate energy of the molecule using the Hartree-Fock method and the sto-3g basis set to a file
    molecule.C8H9 = 60.0+DA
    molecule.C8H10 = 300.0+DA
    molecule.DHC11 = 180.0+DA
    molecule.update_geometry()
    psi4.set_output_file(F'./output_files/Butane_Energy_{DA}.dat', False)
    molecule.save_xyz_file(F'output_files/xyz/{i}_Butane_Energy.xyz',0)
    i+=1
    E = psi4.energy('hf/sto-3g',molecule=molecule)
    energy.append(E)

# Define directory containing the XYZ files and the master file path
xyz_directory = 'output_files/xyz'
master_file_path = 'output_files/xyz/master_Butane_Energy.xyz'

i=0
# Open the master file in write mode
with open(master_file_path, 'w') as master_file:
    # Loop through each XYZ file in the specified directory
    for i in range(len(dihedral_angles)):
        # Open each XYZ file in read mode
        with open(f'output_files/xyz/{i}_Butane_Energy.xyz', 'r') as file:
            # Read contents and write to the master file
            master_file.write(file.read())
        
        # Add a line gap between files
        master_file.write('\n')
        i +=1

# Create the plot
fig = go.Figure()
# Add trace for the dot+line graph
fig.add_trace(go.Scatter(
    x=dihedral_angles,
    y=energy,
    mode='lines+markers',  # This mode will create both lines and dots
    name='Energy vs Dihedral Angle',
    line=dict(color='blue'),
    marker=dict(size=8, color='red')
))
# Customize layout
fig.update_layout(
    title='n-butane - Potential Energy Scan (Dihedral Angle vs Energy)',
    xaxis_title='Dihedral Angle (degrees)',
    yaxis_title='Energy (kJ/mol)',
    width=1200,  # Increase the width for a larger aspect ratio
    height=800,  # Increase the height as needed
    font=dict(size=18)
)
# Show the plot
fig.show()
# Save the plot as a high-resolution PNG
pio.write_image(fig, "n-butane-PES (dihedral angle vs energy).png", 
                width=1280, height=720, scale=3)
