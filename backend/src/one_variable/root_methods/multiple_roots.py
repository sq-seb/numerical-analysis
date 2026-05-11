# THIS FILE DEPENDS ON FIXED_POINT

from fixed_point import fixed_point
import pandas as pd
import sympy as sp
import numpy as np

def multiple_roots(*, f, x0, niter, value, tol_type):
    # multiple_roots = fixed_point with g(x) = x - f(x)f'(x) / ((f'(x))^2 - f(x)f''(x))
    x = sp.symbols('x')

    f_expr = f(x)
    f_prime_expr = sp.diff(f_expr, x)
    f_double_prime_expr = sp.diff(f_prime_expr, x)

    f_num = sp.lambdify(x, f_expr, 'numpy')
    f_prime = sp.lambdify(x, f_prime_expr, 'numpy')
    f_double_prime = sp.lambdify(x, f_double_prime_expr, 'numpy')

    def g(x):
        numerator = f_num(x) * f_prime(x)
        denominator = f_prime(x)**2 - f_num(x) * f_double_prime(x)
        return x - numerator / denominator

    return fixed_point(f=f_num, g=g, x0=x0, niter=niter, value=value, tol_type=tol_type)

if __name__ == "__main__":
    # DEBUGGING

    # (!) THIS MUST BE SP FUNCTION, NOT NP
    def f_symb(x):
        return sp.exp(x)-x-1

    # Test 1
    result = multiple_roots(f=f_symb, x0=1, niter=100, value=1e-7, tol_type="tol")
    print(result["table"])
    print(result["sol"])