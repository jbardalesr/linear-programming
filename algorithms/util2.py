from IPython.display import Latex, display_latex
import sympy as sp


def check_tableau(tableau: sp.Matrix, basic_var: list[int], var: str, holgura=False):
    """
    Input: tabla_simplex, variables_basicas, holgura=True
    1. Verificar que los coeficientes asociados a las variables básicas sean 0.
    2. Verificar que Identidad Permutada esté en las variables básicas, i.e. toda la columna es 0 excepto la fila donde está ubicada la variable básica el cual es 1.
    3. Verificar que los elementos de la última columna sean mayor o igual a 0 (B^{-1}b >= 0).
    """
    for index, col in enumerate(basic_var):
        # Verificando que los coeficientes asociados a las variables básicas sean 0.
        if not tableau[0, col] == 0.0:
            print(f"El costo asociado a la variable básica x{col + 1} no es cero.")
            return False

        # Verificando que toda la columna es 0 excepto la fila donde está ubicada la variable básica el cual es 1.
        for row in range(1, len(basic_var) + 1):
            if row != index + 1:
                if not tableau[row, col] == 0.0:
                    print(f"La columna {col} en la fila {row} asociada a la variable básica x{col + 1} no es 0!")
                    return False
            else:
                if not tableau[row, col] == 1.0:
                    print(f"La columna {col} en la fila {row} asociada a la variable básica x{col + 1} no es 1!")
                    return False

        # Verificando que los elementos de la columna fila B^{-1}*b >= 0.
        if tableau[index + 1, -1] < 0.0:
            print(f"La fila {index + 1} de B^{-1} b es negativo")
            return False
    # Si pasa todas las verificaciones es una tabla simplex.
    print("Si es una tabla simplex, cuyo LO original asociado es")
    tableau2standard(tableau, var, holgura)
    return True


def tableau2standard(tableau: sp.Matrix, var: str, holgura=False):
    dim_1, _ = tableau.shape
    # número de restricciones
    m = dim_1 - 1 if not holgura else 0
    simbol = "\le" if not holgura else "="
    # extrayendo las matrices A, b, y c
    c = tableau[0, :-m - 1]
    A = tableau[1:, :-m - 1]
    b = tableau[1:, -1]
    # variables
    x = sp.Matrix([f"{var}_{i}" for i in range(1, 7 - m)])
    display_latex(Latex(f"$\max{sp.latex(c.dot(x))}\\\\\\text{{subject to}}\\\\{sp.latex(A@x)}{simbol}{sp.latex(b)}$"))


def get_variable(coeff, variable, show_sign=True):
    sign = lambda num: '-' if num < 0 else ('+' if show_sign else '')
    if coeff == 0:
        return ''
    elif abs(coeff) == 1:
        return sign(coeff) + variable
    else:
        return sign(coeff) + str(abs(coeff)) + variable


def get_cost(c, var, indexes):
    n = len(c)
    variable = "%s_{%s}" % (var, indexes[0])
    cost = "{%s}&" % get_variable(c[0], variable, False)
    for i in range(1, n):
        variable = "%s_{%s}" % (var, indexes[i])
        cost += "{%s}&" % get_variable(c[i], variable)
    return cost


def get_constraints(A, b, var, indexes, inequality):
    m, n = A.shape
    constraints = "\\text{s.t.}\\quad"
    for i in range(m):
        variable = "%s_{%s}" % (var, indexes[0])
        constraints += "{%s}&" % get_variable(A[i, 0], variable, False)
        for j in range(1, n):
            variable = "%s_{%s}" % (var, indexes[j])
            constraints += "{%s}&" % get_variable(A[i, j], variable)
        constraints += inequality[i] + "&" + str(b[i]) + "\\\\"
    return constraints


def get_variables(var, indexes):
    return [r"%s_{%s}" % (var, i) for i in indexes]


def print_model(A: sp.Matrix, b: sp.Matrix, c: sp.Matrix, var: str, indexes: list, inequality: list[str], type: str):
    # all variables are positives x_i >= 0 for all i
    cost = get_cost(c, var, indexes)
    constraints = get_constraints(A, b, var, indexes, inequality)
    variables = ','.join(get_variables(var, indexes))
    return display_latex(Latex(r"\begin{align*} \text{%s}\quad %s\\%s \end{align*}\\ %s\ge 0" % (type, cost, constraints, variables)))
