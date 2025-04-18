import numpy as np
from pyscf import gto, scf
import plotly.graph_objects as go
import plotly.io as pio

# Set up the initial molecule structure with approximate bond lengths and angles
def create_molecule(C8H9, C8H10, DHC11):
    return gto.M(
        atom=f'''
            C
            H   1 1.070
            H   1 1.070  2 109.471
            H   1 1.070  2 109.471  3 240.0
            C   1 1.540  2 109.471  3 120.0
            H   5 1.070  1 109.471  2  60.0
            H   5 1.070  1 109.471  2 180.0
            C   5 1.540  1 109.471  2 300.0
            H   8 1.070  5 109.471  1 {C8H9}
            H   8 1.070  5 109.471  1 {C8H10}
            C   8 1.540  5 109.471  1 {DHC11}
            H  11 1.070  8 109.471  5 180.0
            H  11 1.070  8 109.471  5 300.0
            H  11 1.070  8 109.471  5  60.0
        ''',
        basis='sto3g',
        charge=0,
        spin=0,
    )

def array_to_pyscf_string(coordinates_array, atom_symbols):
    pyscf_string = ""
    for i, symbol in enumerate(atom_symbols):
        x, y, z = coordinates_array[i]
        pyscf_string += f"{symbol}  {x:.6f}  {y:.6f}  {z:.6f}\n"
    return pyscf_string

# Function to calculate HF energy at a given dihedral angle
def calculate_energy(C8H9, C8H10, DHC11):
    mol = create_molecule(60.0+C8H9, 300.0+C8H10, 180.0+DHC11)
    atoms_names = [mol.atom_pure_symbol(i) for i in range(mol.natm)]
    with open('PyScf_ZMat.xyz', 'a') as f:
        f.write(f"\n Dihedral {180.0+DHC11}\n {str(array_to_pyscf_string(mol.atom_coords()* 0.529177, atoms_names))}")
    mf = scf.RHF(mol)
    energy = mf.kernel()
    return energy

# Define the range of dihedral angles (0 to 180 degrees, in 10-degree increments)
dihedral_angles = np.arange(0, 361, 10)
energies = []

# Perform PES by iterating over dihedral angles
for angle in dihedral_angles:
    energy = calculate_energy(angle, angle, angle)
    energies.append(energy)

# Create the plot
fig = go.Figure()
# Add trace for the dot+line graph
fig.add_trace(go.Scatter(
    x=dihedral_angles,
    y=energies,
    mode='lines+markers',  # This mode will create both lines and dots
    name='Energy vs Dihedral Angle',
    line=dict(color='blue'),
    marker=dict(size=8, color='red')
))
# Customize layout
fig.update_layout(
    title='n-butane - Potential Energy Scan (Dihedral Angle vs Energy)',
    xaxis_title='Dihedral Angle (degrees)',
    yaxis_title='Energy (Hartree)',
    width=1200,  # Increase the width for a larger aspect ratio
    height=800,  # Increase the height as needed
    font=dict(size=18)
)
# Show the plot
fig.show()
# Save the plot as a high-resolution PNG
pio.write_image(fig, "n-butane-PES (dihedral angle vs energy).png", 
                width=1280, height=720, scale=3)
