import math
from numerical.interfaces.interval_method import IntervalMethod
from shared.utils.convert_math_to_simply import normalize_math_expression, get_math_eval_context
from shared.utils.plot_function import plot_function

class SecantService(IntervalMethod):
    def solve(
        self,
        function_f: str,
        x0: float,
        tolerance: float,
        max_iterations: int,
        precision: bool = False,
        interval_b: float = None,
        **kwargs,
    ) -> dict:

        interval_a = x0

        if interval_b is None:
            return {
                "message_method": "El método de Secante requiere dos puntos iniciales. Por favor, proporcione interval_b.",
                "table": {},
                "is_successful": False,
                "have_solution": False,
                "root": 0.0,
            }

        table = {}
        current_iteration = 1
        current_error = math.inf

        try:
            expression = normalize_math_expression(str(function_f))
            context_a = {"x": interval_a, **get_math_eval_context()}
            context_b = {"x": interval_b, **get_math_eval_context()}
            f_a = eval(expression, context_a)
            f_b = eval(expression, context_b)
        except Exception as e:
            return {
                "message_method": f"Error al evaluar la función en los puntos iniciales: {str(e)}.",
                "table": {},
                "is_successful": False,
                "have_solution": False,
                "root": 0.0,
            }

        if f_a * f_b > 0:
            plot_function(function_f, False, [(interval_a,0), (interval_b,0)])
            return {
                "message_method": "El intervalo es inadecuado, se debe garantizar un cambio de signo para el intervalo dado.",
                "table": {},
                "is_successful": False,
                "have_solution": False,
                "root": 0.0,
            }

        while current_iteration <= max_iterations:
            table[current_iteration] = {}
            if f_b - f_a == 0:
                return {
                    "message_method": "Error: División por cero debido a que f(b) y f(a) son iguales.",
                    "table": table,
                    "is_successful": False,
                    "have_solution": False,
                    "root": 0.0,
                }
            Xn = interval_b - (f_b * (interval_b - interval_a) / (f_b - f_a))

            try:
                expression = normalize_math_expression(str(function_f))
                context = {"x": Xn, **get_math_eval_context()}
                f = eval(expression, context)
            except Exception as e:
                return {
                    "message_method": f"Error al evaluar la función en el punto aproximado: {str(e)}.",
                    "table": table,
                    "is_successful": False,
                    "have_solution": False,
                    "root": 0.0,
                }

            table[current_iteration]["iteration"] = current_iteration
            table[current_iteration]["a"] = interval_a
            table[current_iteration]["b"] = interval_b
            table[current_iteration]["f_a"] = f_a
            table[current_iteration]["f_b"] = f_b
            table[current_iteration]["approximate_value"] = Xn
            table[current_iteration]["f_evaluated"] = f

            if current_iteration == 1:
                table[current_iteration]["error"] = current_error
            else:
                if precision:
                    current_error = abs(table[current_iteration]["approximate_value"] - table[current_iteration - 1]["approximate_value"])
                else:
                    current_error = abs((table[current_iteration]["approximate_value"] - table[current_iteration - 1]["approximate_value"]) / table[current_iteration]["approximate_value"])
                table[current_iteration]["error"] = current_error

            if f == 0 or current_error < tolerance:
                return {
                    "message_method": f"{Xn} es una aproximación de la raíz de f(x) con un error de {current_error}",
                    "table": table,
                    "is_successful": True,
                    "have_solution": True,
                    "root": Xn,
                }

            interval_a = interval_b
            interval_b = Xn

            try:
                expression = normalize_math_expression(str(function_f))
                context_a = {"x": interval_a, **get_math_eval_context()}
                context_b = {"x": interval_b, **get_math_eval_context()}
                f_a = eval(expression, context_a)
                f_b = eval(expression, context_b)
            except Exception as e:
                return {
                    "message_method": f"Error durante la evaluación en el nuevo intervalo: {str(e)}.",
                    "table": table,
                    "is_successful": False,
                    "have_solution": False,
                    "root": 0.0,
                }

            current_iteration += 1

        return {
            "message_method": f"El método funcionó correctamente pero no se encontró solución para {max_iterations} iteraciones",
            "table": table,
            "is_successful": True,
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
        interval_b = kwargs.get("interval_b")

        if interval_b is None:
            return "El método de Secante requiere dos puntos iniciales. Por favor, proporcione interval_b."

        if not isinstance(tolerance, (int, float)) or tolerance <= 0:
            return "La tolerancia debe ser un número positivo"

        if not isinstance(max_iterations, int) or max_iterations <= 0:
            return "El máximo número de iteraciones debe ser un entero positivo."

        try:
            expression = normalize_math_expression(str(function_f))
            context_a = {"x": x0, **get_math_eval_context()}
            context_b = {"x": interval_b, **get_math_eval_context()}
            f_a = eval(expression, context_a)
            f_b = eval(expression, context_b)
        except Exception as e:
            return f"Error al evaluar la función en los puntos iniciales: {str(e)}."

        if f_a == f_b:
            return "División por cero detectada: f(x0) es igual a f(interval_b). Cambie los puntos iniciales."

        return True
