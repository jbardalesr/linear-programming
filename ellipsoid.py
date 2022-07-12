import numpy as np
import math


def update_ellipsoid(x: np.ndarray, D: np.ndarray, d: np.ndarray):
    n = len(x)
    # common products
    Dd = D @ d
    dTDd = np.dot(d, Dd)
    # update step
    x_new = x - 1 / (n + 1) * Dd / math.sqrt(dTDd)
    D_new = n**2 / (n**2 - 1) * (D - 2 / (n + 1) * np.outer(Dd, Dd) / dTDd)
    return x_new, D_new


def check_constraints(A: np.ndarray, b: np.ndarray, x: np.ndarray):
    m = len(b)
    for k in range(m):
        if not np.dot(A[k], x) < b[k]:
            return False, A[k]
    return True, None


def ellipsoidal_algorithm(A, b, x, D, V: float, v: float):
    # return an interior point in the feasible region
    n = len(x)
    t_start = math.ceil(2 * (n + 1) * (np.log(V) - np.log(v)))
    for _ in range(t_start):
        success, d = check_constraints(A, b, x)
        # if pass all constraints x is an interior point
        if success:
            return x, D
        x, D = update_ellipsoid(x, D, d)
    print("P< is empty!")
    return None

def solve_problem(A, b, c, x, D, V0: float, v0: float, MAX_ITER=20):
    for t in range(1, MAX_ITER):
        x, D = ellipsoidal_algorithm(A, b, x, D, V0, v0 / 2**t)
        b = np.r_[b, -np.dot(c, x)]
        A = np.r_[A, [-c]]
        print(f"{t:02d}", x)
