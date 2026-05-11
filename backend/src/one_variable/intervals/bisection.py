import pandas as pd
import numpy as np

def bisection(*, f, a, b, niter, value, tol_type):
    # 1. Check there is at least a trivial solution / no solution to find
    if f(a) * f(b) > 0:
        return {"sol": None, "table": None, "error": f"No root in [{a}, {b}]"}
    elif f(a) == 0:
        return {"sol": None, "table": None, "error": f"No iterations required. Solution found at x={a}"}
    elif f(b) == 0:
        return {"sol": None, "table": None, "error": f"No iterations required. Solution found at x={b}"}

    # 2. Define if we are using either DC, CS, or tol
    if tol_type == "DC":
        tol = 0.5 * 10**-value
    elif tol_type == "CS":
        tol = 5 * 10**-value
    elif tol_type == "tol":
        tol = value

    # 3. Initialize the columns of the table as empty columns
    n_list = []
    x_list = []
    f_list = []
    E_list = []
    ε_list = []
    special_list = []

    # 4. Initialize n, x_prev, sol, xi, xs before iterating through the "main" algorithm
    n = 1
    x_prev = None
    sol = None
    xi = a
    xs = b

    while n <= niter:
        # 5.1 Compute x
        x = (xi + xs) / 2

        # 5.2 Determine the values of En, εn, and ε_{n-1}
        if n >= 2:
            En = abs(x-x_prev)
            εn = En / abs(x)
            special = En / abs(x_prev)
        else:
            En, εn, special = None, None, None

        # 5.3 Append new row to the table
        n_list.append(n)
        x_list.append(x)
        f_list.append(f(x))
        E_list.append(En)
        ε_list.append(εn)
        special_list.append(special)

        # 5.4 Check whether to use En <= tol or εn < tol
        if n >= 2:
            if En <= tol and tol_type in ["DC", "tol"]:
                sol = x
                break
            elif εn < tol and tol_type == "CS":
                sol = x
                break

        # 5.5 Choose next half to iterate through
        if f(xi) * f(x) < 0:
            xs = x
        else:
            xi = x

        # 5.6 Store x_prev and start stage n+1
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
    return {"sol": sol, "table": table, "warning": None}

if __name__ == "__main__":
    # DEBUGGING
    import time

    # Test 1
    def f(x):
        return np.log(np.sin(x)**2 + 1) - 0.5
    result = bisection(f=f, a=0, b=1, niter=100, value=1e-7, tol_type="tol")
    print(result["table"])

    # Sleeping the program for 5 secs
    for i in range(1, 6):
        print(f"[debug]: wait... {i}/5s")
        if i != 5:
            time.sleep(1)
        else:
            time.sleep(0.2)

    # Test 2
    result = bisection(f=lambda x: 77**(-x) * (-1 + x) + (x - 1)**(2 / 3) - 3, a=6.15, b=6.25, niter=100, value=10, tol_type="CS")
    print(result["table"])