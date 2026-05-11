import pandas as pd
import numpy as np

def fixed_point(*, f, g, x0, niter, value, tol_type):
    # 1. Define if we are using either DC, CS, or tol
    if tol_type == "DC":
        tol = 0.5 * 10**-value
    elif tol_type == "CS":
        tol = 5 * 10**-value
    elif tol_type == "tol":
        tol = value

    # 2. Initialize the columns of the table as empty columns
    n_list = []
    x_list = []
    f_list = []
    E_list = []
    ε_list = []
    special_list = []

    # 3. Initialize n, x_{n-1}, and sol before iterating through the "main" algorithm
    n = 0
    x_prev = None
    sol = None
    
    while n <= niter:
        # 4.1 Try xn = g(xn-1)
        if n == 0:
            x = x0
        else:
            try:
                x = g(x_prev)
            except:
                return {"sol": None, "table": None, "error": f"Function g failed at iteration {n}"}

        # 4.2 Determine the values of En, εn, and ε_{n-1}
        if n >= 1:
            En = abs(x-x_prev)
            εn = En / abs(x)
            special = En / abs(x_prev)
        else:
            En, εn, special = None, None, None

        # 4.3 Append new row to the table
        n_list.append(n)
        x_list.append(x)
        f_list.append(f(x))
        E_list.append(En)
        ε_list.append(εn)
        special_list.append(special)

        # 4.4 Check whether to use En <= tol or εn < tol
        if n >= 1:
            if En <= tol and tol_type in ["DC", "tol"]:
                sol = x
                break
            elif εn < tol and tol_type == "CS":
                sol = x
                break

        # 4.4 Store x_prev and start stage n+1
        x_prev = x
        n += 1

    # 6. Create the table and return the solution and the table
    pd.options.display.float_format = lambda x: "NaN" if pd.isna(x) else ("~0 (exceeds e-15)" if abs(x) < 1e-15 else f"{x:.14e}")
    table = pd.DataFrame({
        "xn" : x_list,
        "f(xn)" : f_list,
        "En" : E_list,
        "εn" : ε_list,
        "ε_{n-1}": special_list
    }, index=n_list)
    return {"sol": sol, "table": table, "error": None}

if __name__ == "__main__":
    # DEBUGGING

    def f(x):
        return np.log((np.sin(x))**2 + 1) - (1 / 2) - x
    
    def g(x):
        return np.log((np.sin(x))**2 + 1) - (1 / 2)

    # Test 1
    result = fixed_point(f=f, g=g, x0=-0.5, niter=100, value=1e-7, tol_type="tol")
    print(result["table"])