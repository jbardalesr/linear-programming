import numpy as np
from algorithms.util import *  # absolute path, use * o nothing 


def simplex(tableau: np.ndarray, basic_indices: list[int]) -> np.ndarray:
    print(f"vertex = {basic2vertex(tableau, basic_indices)}, x_B = {real_index(basic_indices)}\n{tableau}")
    while (tableau[0, :-1] > 0).any():
        # max criterion
        c_max = np.argmax(tableau[0, :-1])
        # minimum ratio test
        r_min = minimum_ratio_test(col=tableau[1:, c_max], b=tableau[1:, -1])
        if r_min == None:
            print("The model is unbounded")
            extreme_direction(tableau, basic_indices, c_max)
            break
        # pivoting work on tableau
        pivoting(tableau, r_min + 1, c_max)
        # swap row with col
        basic_indices[r_min] = c_max
        print(f"vertex = {basic2vertex(tableau, basic_indices)}, x_B = {real_index(basic_indices)}\n{tableau}")
    return tableau


def big_M(tableau: np.ndarray, basic_var: list[int], artificial_var: list[int]) -> np.ndarray:
    """
    The big-M procedure, each such constraint $i$ is augmented, together with artificial variable $u_i$, and the objective function is augmented with $-Mu_i$, where $M$ is a big positive real number. For big values of $M$ the simplex algorithm will put highest priority on making the value of the factor $Mu_i$ as small as possible, thereby setting the value of $u_i$ equal to zero.
    """
    print(f"x_B = {real_index(basic_var)}\n{tableau}")
    # correct first row of tableau for each artificial var because the artificial_var position is -M
    correct_cost(tableau, basic_var)
    # solve with simplex
    tableau = simplex(tableau, basic_var)
    # delete the artificial variable
    print("Delete artificial variables", artificial_var)
    tableau = np.delete(tableau, artificial_var, axis=1)
    print(f"x_B = {real_index(basic_var)}\n{tableau}")
    return tableau


def two_phases(tableau: np.ndarray, c: np.ndarray, basic_var: list[int], artificial_var: list[int]) -> np.ndarray:
    """
    All costs are replaced by the negative of the artificial variables until a basic solution is obtained, after which they are replaced by the original cost.    
    """
    print(f"x_B = {real_index(basic_var)}\n{tableau}")
    # correct first row of tableau because the artificial_var position is -1
    correct_cost(tableau, basic_var)
    print(f"x_B = {real_index(basic_var)}\n{tableau}")

    print("Start phase One")
    # while until each artifical var be negative and not be basic var
    while any(((u in basic_var) or (tableau[0, u] > 0)) for u in artificial_var):
        # max criterion
        c_max = np.argmax(tableau[0, :-1])
        # minimum ratio test
        r_min = minimum_ratio_test(col=tableau[1:, c_max], b=tableau[1:, -1])
        # pivoting
        pivoting(tableau, r_min + 1, c_max)
        # swap row with col
        basic_var[r_min] = c_max
        print(f"x_B = {real_index(basic_var)}\n{tableau}")

    print("Delete artificial variables and create a new tableau", artificial_var)
    # delete the artificial variable because we found a solution factible
    tableau = np.delete(tableau, artificial_var, axis=1)
    print("Start phase two, put original cost")
    # put c in first row of tableau
    tableau[0, :len(c)] = c
    # solve with simplex
    print(f"x_B = {real_index(basic_var)}\n{tableau}")
    correct_cost(tableau, basic_var)
    return simplex(tableau, basic_var)


def dual_simplex(tableau: np.ndarray, basic_var: list[int]) -> np.ndarray:
    print(f"vertex = {basic2vertex(tableau, basic_var)}, x_B = {real_index(basic_var)}\n{tableau}")
    while (tableau[1:, -1] < 0).any():
        # max negative criterion
        r_neg = np.argmin(tableau[1:, -1]) + 1
        # dual minimum ratio test
        c_min = dual_minimum_ratio_test(row=tableau[r_neg, :-1], c=tableau[0, :-1])
        if c_min == None:
            print("No feasible solution")
            break
        # pivoting
        pivoting(tableau, r_neg, c_min)
        # swap row with col
        basic_var[r_neg - 1] = c_min
        print(f"vertex = {basic2vertex(tableau, basic_var)}, x_B = {real_index(basic_var)}\n{tableau}")
    return tableau
