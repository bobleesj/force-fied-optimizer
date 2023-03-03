import xyz_py as xyzp
import numpy as np
from scipy.optimize import minimize 
from numpy import sqrt
from numpy import around
import random as rand

# Do not use scientific notation
np.set_printoptions(suppress=True)

# Parse a N-atom argon file.

N = 5
# eps = 0.997 # kJ/mol
# alpha = 3.4 # Angstroms
eps = 1
alpha = 1

# Atom interaction counts:
# 3 atoms: 1-2, 1-3, 2-3 (3)
# 4 atoms: 1-2, 1-3, 1-4, 2-3, 2-4, 3-4 (6)
# 5 atoms: 1-2, 1-3, 1-4, 1-5, 2-3, 2-4, 2,5, 3-4, 3-5, 4-5 (10)

filename = "./xyz/argon_" + str(N) + ".xyz"
atom_labels, cooridnates = xyzp.load_xyz(filename)
print("Parsed Atom labels:\n", atom_labels, "\n") # List
print("Parsed atom coorindates:\n", cooridnates, "\n") # np.array

# Loop and find the distance between all interaction

i_list = list(range(1,N)) # 1 to 3 wher N = 4
j_list = list(range(1,N))
# interaction_count = 0
# LJ_potential_sum = 0
# for i in i_list:
#     for j in j_list:
#         if i <= j:
#             interaction_count += 1
#             ith = i
#             jth = j+1 
#             print("(i,j):", ith, jth)
#             atom_i = cooridnates[ith - 1]
#             atom_j = cooridnates[jth - 1]
            
#             # Calculate the distance (r)
#             r = np.sqrt(np.sum((atom_i-atom_j)**2, axis=0))

#             # Calculate LJ potential
#             LJ = 4 * eps * ((alpha/r)**12 - (alpha/r)**6)
#             # Print r and LJ
#             print("r (Angstroms)", around(r, 3))
#             print("LJ potential (kJ/mol):", round(LJ, 5), "\n")

#             LJ_potential_sum += LJ
            
# print("---OUTOUT---")
# print("LJ potential sum (kJ/mol):", LJ_potential_sum)

# print("SUMMARY:", str(N), "atoms have", str(interaction_count), 
#       "interactions total\n")

# Part II. Apply Neader-Mead for N atoms
# Goal is to find sets of xyz coordinates for N atoms

# Step 1. Intialize the variables based on the interaction

# LJ Potential Implementation
def LJPotential(params):

    LJ_potential_sum = 0
    
    # Reshaped the array
    cooridnates = params.reshape(-1,3)
    for i in i_list:
        for j in j_list:
            if i <= j:
                ith = i
                jth = j+1 
                # print("(i,j):", ith, jth)
                atom_i = cooridnates[ith - 1]
                atom_j = cooridnates[jth - 1]
                
                # Calculate the distance (r)
                r = np.sqrt(np.sum((atom_i-atom_j)**2, axis=0))
                # Calculate LJ potential
                LJ = 4 * eps * ((alpha/r)**12 - (alpha/r)**6)
                # Print r and LJ
                LJ_potential_sum += LJ
    
    return LJ_potential_sum
                
    # # Between 1 and 2
    # x_1 = x1 - x2
    # y_1 = y1 - y2
    # z_1 = z1 - z2
    # # Between 1 and 3
    # x_2 = x1 - x3
    # y_2 = y1 - y3
    # z_2 = z1 - z3
    # # Between 2 and 3
    # x_3 = x2 - x3
    # y_3 = y2 - y3
    # z_3 = z2 - z3

    # LJ_1 = ((alpha/sqrt((x_1)**2 + (y_1)**2 + (z_1)**2))**12
    #                   - (alpha/sqrt((x_1)**2 + (y_1)**2 + (z_1)**2))**6)
    # LJ_2 = ((alpha/sqrt((x_2)**2 + (y_2)**2 + (z_2)**2))**12
    #                   - (alpha/sqrt((x_2)**2 + (y_2)**2 + (z_2)**2))**6)
    # LJ_3 = ((alpha/sqrt((x_3)**2 + (y_3)**2 + (z_3)**2))**12
    #                   - (alpha/sqrt((x_3)**2 + (y_3)**2 + (z_3)**2))**6)
    
    # return 4 * eps * (LJ_1 + LJ_2 + LJ_3)


def minimizeNelderMead(initial_points):
    result = minimize(LJPotential, initial_points, method="nelder-mead", options={'maxiter': 100000})

    if result.success:
        cooridnate_list = result.x
        min_energy = result.fun
        # print(cooridnate_list)
        # print("\n")
        return (min_energy, cooridnate_list)
    else:
        raise ValueError(result.message)

# Generate a random set of coordinates for 3 atoms
# [x1, y1, z1, x2, y2, z2, x3, y3, z3]

for i in range(100):
    random_initial_points = np.random.random_sample(size = N * 3) * 6 - 5 #  
    min_energy, coordinate_list  = minimizeNelderMead(random_initial_points)
    print("Min energy:", min_energy)
    # print("random init position", random_initial_points, "\n")
    # print("optimized coordinate lists:", coordinate_list, "\n")

    # def minimizeNelderMead(initial_points):
    # result = minimize(LJPotential, initial_points, method="nelder-mead", options={'maxiter': 10000})

    # if result.success:
    #     fitted_params = result.x
    #     min_energy = result.fun
    #     x1 = fitted_params[0]
    #     y1 = fitted_params[1]
    #     z1 = fitted_params[2]
    #     x2 = fitted_params[3]
    #     y2 = fitted_params[4]
    #     z2 = fitted_params[5]
    #     x3 = fitted_params[6]
    #     y3 = fitted_params[7]
    #     z3 = fitted_params[8]
    #     print("\n")
    #     return (min_energy)
    # else:
    #     raise ValueError(result.message)