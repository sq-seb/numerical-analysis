import math
from numerical.interfaces.interval_method import IntervalMethod
from shared.utils.convert_math_to_simply import normalize_math_expression, get_safe_eval_globals
from shared.utils.plot_function import plot_function
from typing import Union

class RegulaFalsiService(IntervalMethod):
    def validate_input(
        self, function_f: str, interval_a: float, interval_b: float, tolerance: float, max_iterations: int
    ) -> Union[str, bool]:
        if interval_a >= interval_b:
            return "El extremo inferior del intervalo debe ser menor que el extremo superior."
        if tolerance <= 0:
            return "La tolerancia debe ser un valor positivo."
        if max_iterations <= 0:
            return "El número máximo de iteraciones debe ser un entero positivo."
        try:
            expression = normalize_math_expression(function_f)
            g = lambda x: eval(expression, {**get_safe_eval_globals(), "x": x})
            fa = g(interval_a)
            fb = g(interval_b)
        except Exception as e:
            return f"Error al evaluar la función: {e}"
        if fa * fb > 0:
            return "f(a) y f(b) tienen el mismo signo. No se garantiza la existencia de una raíz en el intervalo."
        if abs(fb - fa) < 1e-12:
            return "Error: División por cero, f(a) y f(b) son demasiado similares."
        return True

    def solve(
        self, function_f: str, interval_a: float, interval_b: float,
        tolerance: float, max_iterations: int, precision: bool = False, **kwargs
    ) -> dict:
        interval = [interval_a, interval_b]
        table = {}
        current_iteration = 1
        current_error = math.inf

        try:
            expression = normalize_math_expression(function_f)
            f = lambda x: eval(expression, {**get_safe_eval_globals(), "x": x})
        except Exception as e:
            return {
                "message_method": f"Error al definir la función: {str(e)}",
                "table": {},
                "is_successful": False,
                "have_solution": False,
                "root": 0.0,
            }

        try:
            fa = f(interval[0])
            fb = f(interval[1])
        except Exception as e:
            return {
                "message_method": f"Error al evaluar f en los extremos del intervalo: {str(e)}",
                "table": {},
                "is_successful": False,
                "have_solution": False,
                "root": 0.0,
            }

        if fa == 0:
            return {
                "message_method": f"{interval[0]} es raíz de f(x) y es el extremo inferior del intervalo.",
                "table": {},
                "is_successful": True,
                "have_solution": True,
                "root": interval[0],
            }
        if fb == 0:
            return {
                "message_method": f"{interval[1]} es raíz de f(x) y es el extremo superior del intervalo.",
                "table": {},
                "is_successful": True,
                "have_solution": True,
                "root": interval[1],
            }

        if abs(fb - fa) < 1e-12:
            return {
                "message_method": "Error: División por cero, f(a) y f(b) son demasiado similares.",
                "table": {},
                "is_successful": False,
                "have_solution": False,
                "root": 0.0,
            }

        while current_iteration <= max_iterations:
            table[current_iteration] = {}

            if abs(fb - fa) < 1e-14:
                return {
                    "message_method": "Error: División por cero detectada durante las iteraciones. f(a) y f(b) son demasiado similares.",
                    "table": table,
                    "is_successful": False,
                    "have_solution": False,
                    "root": 0.0,
                }

            Xn = (interval[0] * fb - interval[1] * fa) / (fb - fa)
            try:
                fxn = f(Xn)
            except Exception as e:
                return {
                    "message_method": f"Error al evaluar la función en Xn: {str(e)}.",
                    "table": table,
                    "is_successful": False,
                    "have_solution": False,
                    "root": 0.0,
                }

            table[current_iteration]["iteration"] = current_iteration
            table[current_iteration]["approximate_value"] = Xn
            table[current_iteration]["f_evaluated"] = fxn

            if current_iteration == 1:
                table[current_iteration]["error"] = current_error
            else:
                if precision:
                    current_error = abs(table[current_iteration]["approximate_value"] - table[current_iteration - 1]["approximate_value"])
                else:
                    current_error = abs((table[current_iteration]["approximate_value"] - table[current_iteration - 1]["approximate_value"]) / table[current_iteration]["approximate_value"])
                table[current_iteration]["error"] = current_error

            if fxn == 0:
                return {
                    "message_method": f"{Xn} es raíz de f(x)",
                    "table": table,
                    "is_successful": True,
                    "have_solution": True,
                    "root": Xn,
                }
            elif current_error < tolerance:
                return {
                    "message_method": f"{Xn} es una aproximación de la raíz con error {current_error}",
                    "table": table,
                    "is_successful": True,
                    "have_solution": True,
                    "root": Xn,
                }

            if fa * fxn < 0:
                interval[1] = Xn
                fb = fxn
            else:
                interval[0] = Xn
                fa = fxn

            current_iteration += 1

        return {
            "message_method": f"El método funcionó pero no encontró raíz en {max_iterations} iteraciones",
            "table": table,
            "is_successful": True,
            "have_solution": False,
            "root": 0.0,
        }
