import sympy as sp
import pandas as pd
import numpy as np

def safe_eval(f, x):
    """
    Strict evaluation:
    - returns float if valid
    - returns None if NaN/inf/complex/error
    """
    try:
        y = f(x)
        y = np.asarray(y)

        if np.iscomplexobj(y):
            return None

        if not np.all(np.isfinite(y)):
            return None

        return float(y)

    except Exception:
        return None

def check_continuity(f, a, b):
    """
    Check if the function is continuous in the domain [a, b].
    This checks for division by zero and undefined behavior.
    """
    x = sp.symbols('x')

    # Convert f(x) into a sympy expression
    f_sympy = f(x)

    # Print the function expression
    print(f"Function expression: {f_sympy}")

    # Check if the function is a rational function
    if isinstance(f_sympy, sp.Rational):
        denominator = sp.denom(f_sympy)
        print(f"Denominator: {denominator}")

        # We handle linear denominators explicitly
        if denominator.has(x):  # If the denominator contains x (i.e., is a rational function)
            singularities = sp.solve(denominator, x)
            print(f"Solved singularity expression: {singularities}")
            
            # Check if the singularity lies in the given interval [a, b]
            for s in singularities:
                print(f"Checking singularity {s} within the interval [{a}, {b}]")
                if a <= s <= b:
                    warning_msg = f"Warning: Singularities found at {s} in the interval [{a}, {b}]"
                    return True, warning_msg

    # Check limits at the endpoints and ensure the function is well-defined at the boundaries
    try:
        left_limit = sp.limit(f_sympy, x, a, dir='+')
        right_limit = sp.limit(f_sympy, x, b, dir='-')
        print(f"Left limit at {a}: {left_limit}, Right limit at {b}: {right_limit}")

        # If the function goes to infinity or is undefined at any endpoint, return True for discontinuity
        if left_limit == sp.oo or left_limit == -sp.oo or left_limit is sp.nan:
            return True, f"Discontinuity or undefined behavior at the left endpoint."
        if right_limit == sp.oo or right_limit == -sp.oo or right_limit is sp.nan:
            return True, f"Discontinuity or undefined behavior at the right endpoint."

    except Exception as e:
        print(f"Error in continuity check: {e}")
        return True, f"Error in continuity check: {e}"  # If something goes wrong, assume discontinuity

    # Function is continuous if no issues were found
    return False, None

def is_interval_contained(A, B):
    """
    Checks if interval A is contained within interval B
    A = [a1, b1], B = [a2, b2]
    Returns True if A is contained in B, else False.
    """
    a1, b1 = A
    a2, b2 = B
    return a2 <= a1 <= b1 <= b2

def bisection(*, f, a, b, niter, value, tol_type, max_val=1e16):
    # Check if the interval [a, b] has a discontinuity
    print(f"Checking for discontinuities in the interval [{a}, {b}]")
    discontinuous, warning_msg = check_continuity(f, a, b)
    
    if discontinuous:
        print(f"Discontinuity detected: {warning_msg}")
        return {
            "sol": None,
            "table": None,
            "warning": warning_msg
        }

    # ---------------------------- 
    # 0. SAFE ENDPOINT EVALUATION
    # ---------------------------- 
    fa = safe_eval(f, a)
    fb = safe_eval(f, b)
    print(f"Evaluating function at endpoints: f({a}) = {fa}, f({b}) = {fb}")

    if fa is None or fb is None:
        return {
            "sol": None,
            "table": None,
            "warning": "The function is not defined in at least one of the bounds, or it exceeds max{|f(a)|,|f(b)|} > 10^16"
        }

    # ---------------------------- 
    # 1. VALID BRACKETING CHECK
    # ---------------------------- 
    if fa * fb > 0:
        return {
            "sol": None,
            "table": None,
            "warning": f"No sign change in [{a}, {b}], so no guaranteed root by this method (even though it may exist)"
        }

    if fa == 0:
        return {"sol": a, "table": None, "warning": "Root found at left endpoint before 1st iteration."}

    if fb == 0:
        return {"sol": b, "table": None, "warning": "Root found at right endpoint before 1st iteration."}

    # ---------------------------- 
    # 2. TOLERANCE SETUP
    # ---------------------------- 
    if tol_type == "DC":
        tol = 0.5 * 10**-value
    elif tol_type == "CS":
        tol = 5 * 10**-value
    elif tol_type == "tol":
        tol = value
    else:
        return {"sol": None, "table": None, "warning": "Invalid tol_type"}

    # ---------------------------- 
    # 3. STORAGE
    # ---------------------------- 
    n_list = []
    x_list = []
    f_list = []
    E_list = []
    eps_list = []
    eps_prev_list = []  # This will store the ε_{n-1} values

    # ---------------------------- 
    # 4. INITIAL VALUES
    # ---------------------------- 
    xi, xs = a, b
    x_prev = None
    sol = None

    # ---------------------------- 
    # 5. MAIN LOOP
    # ---------------------------- 
    for n in range(1, niter + 1):
        x = (xi + xs) / 2
        fx = safe_eval(f, x)

        # ---------------------------- 
        # HANDLE EXPLOSION (fx > max_val)
        # ---------------------------- 
        if fx is None or abs(fx) > max_val:
            n_list.append(n)
            x_list.append(x)
            f_list.append("strNaN")
            E_list.append("strNaN")
            eps_list.append("strNaN")
            eps_prev_list.append("strNaN")
            # Add a warning and stop the iterations
            warning = f"Function value exploded to infinity or exceeded threshold at iteration {n}."
            break
        else:
            warning = None

        # ---------------------------- 
        # HANDLE BAD FUNCTION VALUE
        # ---------------------------- 
        if fx is None:
            n_list.append(n)
            x_list.append(x)
            f_list.append("strNaN")
            E_list.append("strNaN")
            eps_list.append("strNaN")
            eps_prev_list.append("strNaN")
            break  # Stop the iteration if function evaluation fails

        # ---------------------------- 
        # ERROR METRICS
        # ---------------------------- 
        if n == 1:
            En = None
            eps = None
            eps_prev = None
        else:
            En = abs(x - x_prev)
            eps = En / abs(x) if x != 0 else None
            eps_prev = En / abs(x_prev) if x_prev != 0 else None

        # ---------------------------- 
        # STORE ROW (NO None ALLOWED)
        # ---------------------------- 
        n_list.append(n)
        x_list.append(x)
        f_list.append(fx if fx is not None else "strNaN")
        E_list.append(En if En is not None else "strNaN")
        eps_list.append(eps if eps is not None else "strNaN")
        eps_prev_list.append(eps_prev if eps_prev is not None else "strNaN")  # Store the ε_{n-1}

        # ---------------------------- 
        # STOPPING CRITERIA
        # ---------------------------- 
        if n > 1:
            if tol_type in ["DC", "tol"] and En is not None and En <= tol:
                sol = x
                break
            if tol_type == "CS" and eps is not None and eps < tol:
                sol = x
                break

        # ---------------------------- 
        # UPDATE INTERVAL (SAFE)
        # ---------------------------- 
        fxi = safe_eval(f, xi)

        if fxi is None:
            n_list.append(n)
            x_list.append(xi)
            f_list.append("strNaN")
            E_list.append("strNaN")
            eps_list.append("strNaN")
            eps_prev_list.append("strNaN")
            break

        # Update the interval based on bisection method
        if fxi * fx < 0:
            xs = x
        else:
            xi = x

        x_prev = x

    # ---------------------------- 
    # 6. OUTPUT TABLE & WARNING CHECK
    # ---------------------------- 
    pd.options.display.float_format = lambda x: (
        "strNaN" if x == "strNaN"
        else ("~0" if isinstance(x, (int, float)) and abs(x) < 1e-15 else x)
    )

    # Check if we finished all iterations without finding a solution
    if sol is None:
        if warning is None:
            warning = f"Max iterations ({niter}) reached without finding a root of tolerance {int(value)} {tol_type}. Anyways, closest x found is {xi} with an absolute error E of {En}."
    else:
        warning = None

    table = pd.DataFrame({
        "n": n_list,
        "xn": x_list,
        "f(xn)": f_list,
        "En": E_list,
        "εn": eps_list,
        "ε_{n-1}": eps_prev_list  # Add the missing ε_{n-1} column
    }).to_dict("records")

    return {"sol": sol, "table": table, "warning": warning}

# Sample function for testing
def test_function(x):
    return 1 / (x + 0.05)

# Run with debugging enabled
bisection(f=test_function, a=-1, b=1, niter=50, value=5, tol_type="DC")