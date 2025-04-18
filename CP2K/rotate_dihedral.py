# rotate_dihedral.py
import sys
from ase.io import read, write
import numpy as np
def rotate_dihedral(xyz_file, angle, output_xyz):
    molecule = read(xyz_file)
    molecule.set_dihedral(0, 4, 7, 10, angle, mask=[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1])
    write(output_xyz, molecule)
if __name__ == "__main__":
    xyz_file = sys.argv[1]
    angle = float(sys.argv[2])
    output_xyz = sys.argv[3]
    rotate_dihedral(xyz_file, angle, output_xyz)
