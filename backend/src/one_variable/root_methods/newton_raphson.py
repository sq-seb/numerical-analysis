# THIS FILE DEPENDS ON FIXED_POINT

from fixed_point import fixed_point
import pandas as pd
import sympy as sp
import numpy as np

def newton_raphson(*, f, x0, niter, value, tol_type):
    # newton_raphson = fixed_point with g(x) = x - f(x) / f'(x)
    x = sp.symbols('x')

    f_expr = f(x)
    f_prime_expr = sp.diff(f_expr, x)

    f_num = sp.lambdify(x, f_expr, 'numpy')
    f_prime = sp.lambdify(x, f_prime_expr, 'numpy')

    def g(x):
        return x - f_num(x)/f_prime(x)
    
    return fixed_point(f=f_num, g=g, x0=x0, niter=niter, value=value, tol_type=tol_type)

if __name__ == "__main__":
    # DEBUGGING

    # (!) THIS MUST BE SP FUNCTION, NOT NP
    def f_symb(x):
        return sp.log((sp.sin(x))**2 + 1) - 0.5

    # Test 1
    result = newton_raphson(f=f_symb, x0=0.5, niter=100, value=1e-7, tol_type="tol")
    print(result["table"])
    print(result["sol"])