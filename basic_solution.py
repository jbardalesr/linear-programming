from itertools import combinations
import math
import sympy as sp
from IPython.display import display_latex, Latex


def pretty_print(string: str):
    return display_latex(Latex(string))


def factible_vertex(A: sp.Matrix, b: sp.Matrix, c: sp.Matrix):
    m, n = A.shape
    comb = tuple(combinations(range(m), n))
    print("Number of combinations:", len(comb))
    # for each combiantion for indexes
    for indexes in comb:
        A_inv = sp.Matrix.inv(A.row(indexes))
        x = A_inv @ b.row(indexes)
        show = True
        # for each constraint
        for j in range(m):
            if not A.row(j).dot(x) <= b[j]:
                show = False
                break
        if show:
            pretty_print(f"$A^{{-1}}={sp.latex(A_inv)}\quad x{indexes}={sp.latex(x)}\quad c={c.dot(x).evalf()}$")


def basic_solutions(A, b):
    m, n = A.shape
    print("Number of combinations: %d" % math.comb(n, m))
    for i, comb in enumerate(combinations(range(n), m)):
        print(f"Basic solution {i + 1}")
        B = A.col(comb)
        x_labels = sp.Matrix([f"x_{i+1}" for i in comb])
        try:
            B_inv = B.inv()
            x_b = B_inv @ b  # x_n are zeros
            pretty_print(f"$$B={sp.latex(B)}, \quad \mathbf x_B={sp.latex(x_labels)} = B^{{-1}}\mathbf b={sp.latex(B_inv)}{sp.latex(b)}={sp.latex(x_b)}$$")
        except Exception as ex:
            print(ex)
            pretty_print(f"$$B = {sp.latex(B)}, {sp.latex(x_labels)}$$")
            continue
