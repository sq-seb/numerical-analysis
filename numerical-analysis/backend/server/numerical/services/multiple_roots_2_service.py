import sympy as sp
import math
from numerical.interfaces.iterative_method import IterativeMethod
from shared.utils.convert_math_to_simply import convert_math_to_sympy
from shared.utils.plot_function import plot_function


class MultipleRoots2Service(IterativeMethod):
    def solve(self, **kwargs) -> dict:
        x0 = kwargs.get("x0")
        tolerance = kwargs.get("tolerance")
        max_iterations = kwargs.get("max_iterations")
        precision = kwargs.get("precision")
        function_f = kwargs.get("function_f")

        x = sp.symbols("x")
        sympy_function_f = convert_math_to_sympy(function_f)
        f_expr = sp.sympify(sympy_function_f)
        f_prime_expr = sp.diff(f_expr, x)
        f_double_prime_expr = sp.diff(f_prime_expr, x)

        f = sp.lambdify(x, f_expr, modules=["math"])
        f_prime = sp.lambdify(x, f_prime_expr, modules=["math"])
        f_double_prime = sp.lambdify(x, f_double_prime_expr, modules=["math"])

        table = {}
        x0_current = x0
        current_error = math.inf
        current_iteration = 1

        while current_iteration <= max_iterations:
            try:
                fx = f(x0_current)
                f_prime_x = f_prime(x0_current)
                f_double_prime_x = f_double_prime(x0_current)

                denominator = f_prime_x ** 2 - fx * f_double_prime_x
                if abs(f_prime_x) < 1e-12 or abs(denominator) < 1e-12:
                    return {
                        "message_method": f"División por cero evitada: derivada o denominador cero cercano en x = {x0_current}. No se puede continuar.",
                        "table": table,
                        "is_successful": False,
                        "have_solution": False,
                        "root": 0.0,
                    }

                x_next = x0_current - (fx * f_prime_x) / denominator

            except Exception as e:
                return {
                    "message_method": f"Error al evaluar la función o sus derivadas: {str(e)}.",
                    "table": table,
                    "is_successful": False,
                    "have_solution": False,
                    "root": 0.0,
                }

            table[current_iteration] = {
                "iteration": current_iteration,
                "approximate_value": x0_current,
                "f_evaluated": fx,
                "f_prime_evaluated": f_prime_x,
                "f_double_prime_evaluated": f_double_prime_x,
                "next_x": x_next,
            }

            if current_iteration > 1:
                if precision:
                    current_error = abs(x_next - x0_current)
                else:
                    current_error = abs((x_next - x0_current) / x_next) if x_next != 0 else abs(x_next - x0_current)
                table[current_iteration]["error"] = current_error
            else:
                table[current_iteration]["error"] = current_error

            if fx == 0:
                return {
                    "message_method": f"{x0_current} es una raíz exacta de f(x).",
                    "table": table,
                    "is_successful": True,
                    "have_solution": True,
                    "root": x0_current,
                }
            if current_iteration > 1 and current_error < tolerance:
                return {
                    "message_method": f"{x0_current} es una aproximación de la raíz de f(x) con un error menor a {tolerance}.",
                    "table": table,
                    "is_successful": True,
                    "have_solution": True,
                    "root": x0_current,
                }

            x0_current = x_next
            current_iteration += 1

        return {
            "message_method": f"El método funcionó pero no se encontró solución en {max_iterations} iteraciones.",
            "table": table,
            "is_successful": False,
            "have_solution": False,
            "root": 0.0,
        }

    def validate_input(
        self,
        x0: float,
        tolerance: float,
        max_iterations: int,
        function_f: str,
        **kwargs,
    ) -> str | bool:
        x = sp.symbols("x")
        sympy_function_f = convert_math_to_sympy(function_f)

        if not isinstance(tolerance, (int, float)) or tolerance <= 0:
            return "La tolerancia debe ser un número positivo"

        if not isinstance(max_iterations, int) or max_iterations <= 0:
            return "El máximo número de iteraciones debe ser un entero positivo."

        try:
            f_expr = sp.sympify(sympy_function_f)
            if f_expr.free_symbols != {x}:
                return "Error al interpretar la función: utilice la variable 'x'."
            sp.diff(f_expr, x)
            sp.diff(sp.diff(f_expr, x), x)
        except Exception as e:
            return f"Error al interpretar o derivar la función: {str(e)}."

        try:
            sp.lambdify(x, f_expr, modules=["math"])
            sp.lambdify(x, sp.diff(f_expr, x), modules=["math"])
            sp.lambdify(x, sp.diff(sp.diff(f_expr, x), x), modules=["math"])
        except Exception as e:
            return f"Error al convertir la función o sus derivadas a formato numérico: {str(e)}."

        return True
