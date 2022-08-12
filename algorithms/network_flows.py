import numpy as np
from IPython.display import display_latex, Latex


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
    A = np.zeros((number_node, number_edge))
    for k in range(number_edge - 1):
        A[edges[k].i - 1, k] = 1
        A[edges[k].j - 1, k] = -1
    A[edges[-1].i - 1, -1] = 1
    return A
