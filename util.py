import numpy as np


def build_tableau(A: list, b: list, c: list) -> np.ndarray:
    """
    Input: mxn matrix A, mx1 vector b>=0, nx1 vector c
    Output: A simplex table of a LO with slack variables Ax + x_s = b
    """
    tableau = np.r_[[c], A]
    tableau = np.c_[tableau, np.insert(b, 0, 0)]
    return tableau


def minimum_ratio_test(col: np.ndarray, b: np.ndarray) -> int:
    r_min = 0
    min_val = np.inf
    for k in range(len(b)):
        if col[k] > 0:
            min_val_temp = b[k] / col[k]
            if min_val_temp < min_val:
                min_val = min_val_temp
                r_min = k
    return r_min if min_val != np.inf else None


def dual_minimum_ratio_test(row: np.ndarray, c: np.ndarray) -> int:
    c_min = 0
    min_val = np.inf
    for k in range(len(c)):
        if row[k] < 0:
            min_val_temp = c[k] / row[k]
            if min_val_temp < min_val:
                min_val = min_val_temp
                c_min = k
    return c_min if min_val != np.inf else None


def pivoting(tableau: np.ndarray, row: int, col: int) -> None:
    # escale row pivot to 1.0
    tableau[row] = tableau[row] / tableau[row, col]
    # pivot proccess: convert al column to zero except row or those that are already zero
    for k in range(len(tableau)):
        if k != row and abs(tableau[k, col]) > 0:
            tableau[k] = tableau[k] - tableau[k, col] * tableau[row]


def correct_cost(tableau: np.ndarray, basic_var: list[int]) -> None:
    # correct basic variable cost with value distict of zero
    for index, col in enumerate(basic_var):
        if abs(tableau[0, col]) > 0:
            row = index + 1
            tableau[0] = tableau[0] - tableau[0, col] * tableau[row]
    print(f"Cost corrected")


def correct_all_tableau(tableau: np.ndarray, basic_var: list[int]) -> None:
    # correct basic variable of all column with value distict of zero
    for index, col in enumerate(basic_var):
        row = index + 1
        pivoting(tableau, row, col)
    print("All tableau corrected")


def basic2vertex(tableau: np.ndarray, basic_var: list[int], show_all=False) -> np.array:
    dim_1, dim_2 = tableau.shape
    m = len(basic_var)
    n = dim_2 - dim_1
    x = np.zeros(m + n)
    x[basic_var] = tableau[1:, -1]
    return x[:n] if not show_all else x


def optimal_solution(tableau: np.ndarray, basic_var: list[int]) -> None:
    print("Optimal solution: x_opt =", basic2vertex(tableau, basic_var))


def real_index(basic_var: list[int]) -> list:
    # add 1 to all index of basic variables [x0, x1, x2] -> [x1, x2, x3]
    return list(map(lambda x: x + 1, basic_var))


def extreme_direction(tableau: np.ndarray, basic_var: list[int], col: int) -> None:
    # for unbounded model
    dim_1, dim_2 = tableau.shape
    m = len(basic_var)
    n = dim_2 - dim_1
    x = np.zeros(m + n)
    dir = np.zeros(m + n)
    x[basic_var] = tableau[1:, -1]
    dir[basic_var] = tableau[1:, col]
    print(f"L = {x} + λ{-dir}\nL = {x[:n]} + λ{-dir[:n]}")
