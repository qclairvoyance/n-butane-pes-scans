import numpy as np
from scipy.spatial.transform import Rotation as R

def inp_file(coords):
    return f"""!   File created by the GAMESS Input Deck Generator Plugin for Avogadro
 $BASIS GBASIS=STO NGAUSS=3 $END
 $CONTRL SCFTYP=RHF RUNTYP=ENERGY $END

 $DATA
Title
C1
{coords} $END"""

atom_names = ["H", "C", "H", "H", "C", "H", "H", "C", "H", "H", "C", "H", "H", "H"]

atomic_weights = [1.0, 6.0, 1.0, 1.0, 6.0, 1.0, 1.0, 6.0, 1.0, 1.0, 6.0, 1.0, 1.0, 1.0]

 coordinates
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

def array_to_gamess_string(coordinates_array, atom_symbols, atomic_weights):
    gamess_string = ""
    for i, symbol in enumerate(atom_symbols):
        x, y, z = coordinates_array[i]

        gaamess_string += f"{symbol}     {atomic_weights[i]:.1f}    {x:.6f}     {y:.6f}     {z:.6f}\n"
    return pyscf_string

def array_to_gamess_string(coordinates_array, atom_symbols):
    gamess_string = ""
    for i, symbol in enumerate(atom_symbols):
        x, y, z = coordinates_array[i]
        if i == 0:
            gamess_string += f"  {symbol:<2} {x:>17.10f} {y:>17.10f} {z:>17.10f}\n"
        else:
            gamess_string += f"  {symbol:<2} {x:>17.10f} {y:>17.10f} {z:>17.10f}\n"
    return gamess_string

def dihedral_butane_2(coords, names, atom_weights, angle):
    atom_pos = coords.copy()
    A, B = atom_pos[4], atom_pos[7]
    rotation_axis = A - B
    rotation = R.from_rotvec(np.radians(angle) * rotation_axis / np.linalg.norm(rotation_axis))
    atom_pos[8:] = rotation.apply(atom_pos[8:] - A) + A
    atoms_names = names
    return  array_to_gamess_string(atom_pos, atom_names)

with open(f"all_configs_gamess.xyz", "a") as file:
    for angle in range(0, 361, 10):
        file.write(f"\n Rotation Angle = {angle}\n")
        file.write(dihedral_butane_2(coordinates, atom_names, atomic_weights, angle)[1])

for angle in range(0, 361, 10):
    input_string = inp_file(dihedral_butane_2(coordinates, atom_names, atomic_weights, angle)[0])
    print(input_string)
    but_str = input_string
    angle_str = str(angle).zfill(3)
    with open(f"butane_rotation_{angle_str}.inp", 'w') as file:
        file.write(but_str)
