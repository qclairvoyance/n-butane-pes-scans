import numpy as np
from pyscf import gto, dft, scf, mp
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt

butane = """
 C    1.37186865    1.05580896    3.45290470
 H    0.99389687    0.22153219    4.00609509
 H    2.41053448    0.90476699    3.24491524
 H    1.24959090    1.94988795    4.02785767
 C    0.59695173    1.18712599    2.12857106
 H    -0.44171410    1.33816797    2.33656052
 H    0.97492351    2.02140276    1.57538067
 C    0.77294026   -0.09967928    1.30106865
 H    1.81160609   -0.25072125    1.09307919
 H    0.39496848   -0.93395605    1.85425904
 C    -0.00197666    0.03163775   -0.02326499
 H    0.12032462   -0.86243011   -0.59823025
 H    -1.04064660    0.18265150    0.18472445
 H    0.37597595    0.86593162   -0.57644269
"""

butane_mol = gto.M(atom = butane, basis = 'sto-3g')
butane_mol.build()
mf = scf.RHF(butane_mol)
mf.kernel()

def array_to_pyscf_string(coordinates_array, atom_symbols):
    pyscf_string = ""
    for i, symbol in enumerate(atom_symbols):
        x, y, z = coordinates_array[i]
        pyscf_string += f"{symbol}  {x:.6f}  {y:.6f}  {z:.6f}\n"
    return pyscf_string

def dihedral_butane_2(mol, angle):
    atom_pos = mol.atom_coords() * 0.529177
    A, B = atom_pos[4], atom_pos[7]
    rotation_axis = A - B
    rotation = R.from_rotvec(np.radians(angle) * rotation_axis / np.linalg.norm(rotation_axis))
    print(np.radians(angle) * rotation_axis / np.linalg.norm(rotation_axis))
    atom_pos[8:] = rotation.apply(atom_pos[8:] - A) + A
    atoms_names = [mol.atom_pure_symbol(i) for i in range(mol.natm)]
    return array_to_pyscf_string(atom_pos, atoms_names)

def but_energy_dft(atom):
    mol = gto.Mole(atom = atom, basis = '631G*')
    mol.build()
    mf = dft.RKS(mol)
    mf.xc = 'b3lyp'
    return mf.kernel()

def but_energy(atom):
    mol = gto.Mole(atom = atom, basis = 'sto-3g')
    mol.build()
    mf = scf.RHF(mol)
    hf_energy = mf.kernel()
    return mf.kernel()

def but_energy_mp2(atom):
    mol = gto.Mole(atom = atom, basis = 'cc-pvdz')
    mol.build()
    mf = scf.RHF(mol)
    hf_energy = mf.kernel()

    mp2 = mp.MP2(mf)
    mp2_energy, 
    = mp2.kernel()
    return mp2_energy + hf_energy

but_energies_dft = []
but_energies_mp2 = []
but_energies = []
for angle in range(-180, 181, 10):
    output = dihedral_butane_2(butane_mol, angle)
    but_energies_dft.append([angle, but_energy_dft(output)])
    but_energies_mp2.append([angle, but_energy_mp2(output)])
    but_energies.append([angle, but_energy(output)])
