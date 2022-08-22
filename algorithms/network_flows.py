import sympy as sp
from IPython.display import display_latex, Latex


def pretty_print(str):
    display_latex(Latex(str))


def print_vector(msg: str, var: str, array: list, indexes: list = None):
    if indexes == None:
        indexes = list(range(len(array)))
    new_array = ["%s_{%s}=%s" % (var, indexes[i], element) for i, element in enumerate(array)]
    str_array = ', '.join(new_array)
    return display_latex(Latex(r"$\text{%s}\\{%s}$" % (msg, str_array)))


class Edge:
    def __init__(self, i: int, j: int, cost: float) -> None:
        self.i = i
        self.j = j
        self.cost = cost

    def __str__(self) -> str:
        return f"{self.i} → {self.j}, c={self.cost}"


def get_edges(edges: list[Edge], indexes: list):
    return [(edges[k].i, edges[k].j) for k in indexes]


def build_matrix(number_node: int, edges: list[Edge]):
    # Output: matrix mx(n+1) A, with component i=1, j=-1, and last component 1
    number_edge = len(edges)
    A = sp.zeros(number_node, number_edge)
    for k in range(number_edge - 1):
        A[edges[k].i - 1, k] = 1
        A[edges[k].j - 1, k] = -1
    A[edges[-1].i - 1, -1] = 1
    return A


def calculate_tree(A: sp.Matrix, b: sp.Matrix, c: sp.Matrix, basic_var: list[int], non_basic_var: list[int]):
    B = A.col(basic_var)
    print("Matriz B")
    pretty_print(f"$B={sp.latex(B)}$")
    N = A.col(non_basic_var)
    B_inv = B.inv()
    # x = B^{-1} b
    x_sol = B_inv @ b
    # w^T = c_BI^T B^{-1} 
    w_T = c.row(basic_var).T @ B_inv
    # z = w^T N - c_NI^T
    z = w_T @ N - c.row(non_basic_var).T
    return x_sol, w_T, z
