import numpy as np
from scipy.spatial.transform import Rotation as R
import sys

# Function to format NWChem input file
def inp_file(coord):
    return f"""echo
start molecule
title "Title"
charge 0
geometry units angstroms print xyz autosym
{coord}
end

basis
  * library STO-3G
end

dft
  xc b3lyp
  mult 1
end

task dft energy
"""

# Arrays for atom names and coordinates
atom_names = ["H", "C", "H", "H", "C", "H", "H", "C", "H", "H", "C", "H", "H", "H"]
coordinates = np.array([
    [0.20500, -0.89142, 2.77756],
    [-0.27366, -0.93316, 1.79095],
    [-0.94475, -1.80245, 1.78815],
    [-0.90133, -0.03743, 1.69257],
    [0.75376, -1.01817, 0.68509],
    [1.43820, -0.14805, 0.73591],
    [1.39608, -1.90923, 0.83200],
    [0.09688, -1.07703, -0.68499],
    [0.45719, -0.23623, -1.31061],
    [0.41471, -1.99733, -1.21430],
    [-1.41080, -1.03505, -0.58082],
    [-1.80013, -1.87971, 0.00310],
    [-1.75777, -0.11462, -0.09251],
    [-1.88025, -1.07749, -1.57183]
])

# Function to convert array to NWChem string
def array_to_nwchem_string(coordinates_array, atom_symbols):
    nwchem_string = ""
    for i, symbol in enumerate(atom_symbols):
        x, y, z = coordinates_array[i]
        nwchem_string += f"  {symbol:<2} {x:>17.10f} {y:>17.10f} {z:>17.10f}\n"
    return nwchem_string

# Function to calculate rotated coordinates
def dihedral_butane_2(coord, names, angle):
    atom_pos = coord.copy()
    A, B = atom_pos[4], atom_pos[7]
    rotation_axis = A - B
    rotation = R.from_rotvec(np.radians(angle) * rotation_axis / np.linalg.norm(rotation_axis))
    atom_pos[8:] = rotation.apply(atom_pos[8:] - A) + A
    return array_to_nwchem_string(atom_pos, names)

# Main script execution
if __name__ == "__main__":
    angle = float(sys.argv[1])  # Angle provided as a command-line argument
    coordinates_str = dihedral_butane_2(coordinates, atom_names, angle)
    nwchem_input_content = inp_file(coordinates_str)
    
    # Print the NWChem input content to be captured by the shell script
    print(nwchem_input_content)
