import math
from shared.utils.convert_math_to_simply import normalize_math_expression, get_math_eval_context
from shared.utils.plot_function import plot_function
from numerical.interfaces.iterative_method import IterativeMethod

class FixedPointService(IterativeMethod):
    def solve(
        self,
        function_f: str,
        function_g: str,
        x0: float,
        tolerance: float,
        max_iterations: int,
        precision: bool = False,
    ) -> dict:
        
        table = {}
        current_iteration = 1
        current_error = math.inf

        while current_iteration <= max_iterations:
            table[current_iteration] = {}

            try:
                x = x0
                g_expression = normalize_math_expression(function_g)
                g = eval(g_expression, {"x": x, **get_math_eval_context()})

                x = g
                f_expression = normalize_math_expression(function_f)
                f = eval(f_expression, {"x": x, **get_math_eval_context()})
            except Exception as e:
                return {
                    "message_method": f"El x evaluado en g(x) no pertenece al dominio de la función, la descripción de este error fue: {str(e)}.",
                    "table": table,
                    "is_successful": True,
                    "have_solution": False,
                    "root": 0.0,
                }

            table[current_iteration]["iteration"] = current_iteration
            table[current_iteration]["approximate_value"] = g
            table[current_iteration]["f_evaluated"] = f

            if current_iteration == 1:
                table[current_iteration]["error"] = current_error

            else:
                if precision:
                    current_error = abs(
                        table[current_iteration]["approximate_value"]
                        - table[current_iteration - 1]["approximate_value"]
                    )
                    table[current_iteration]["error"] = current_error
                else:
                    current_error = abs(
                        (
                            table[current_iteration]["approximate_value"]
                            - table[current_iteration - 1]["approximate_value"]
                        )
                        / table[current_iteration]["approximate_value"]
                    )
                    table[current_iteration]["error"] = current_error

            if f == 0:
                return {
                    "message_method": "{} es raiz de f(x)".format(g),
                    "table": table,
                    "is_successful": True,
                    "have_solution": True,
                    "root": g,
                }

            elif current_error < tolerance:
                return {
                    "message_method": "{} es una aproximación de la raiz de f(x) con un error de {}".format(
                        g, current_error
                    ),
                    "table": table,
                    "is_successful": True,
                    "have_solution": True,
                    "root": g,
                }
            else:
                x0 = g
                current_iteration += 1
        
        return {
            "message_method": "El método funcionó correctamente pero no se encontró solución para {} iteraciones".format(
                max_iterations
            ),
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

        function_g = kwargs.get("function_g")

        if not isinstance(tolerance, (int, float)) or tolerance <= 0:
            return "La tolerancia debe ser un número positivo"

        if not isinstance(max_iterations, int) or max_iterations <= 0:
            return "El máximo número de iteraciones debe ser un entero positivo."

        try:
            x = x0
            g_expression = normalize_math_expression(function_g)
            g = eval(g_expression, {"x": x, **get_math_eval_context()})

            x = g
            f_expression = normalize_math_expression(function_f)
            f = eval(f_expression, {"x": x, **get_math_eval_context()})
        except ValueError:
            return "Error: Valor fuera del dominio permitido para la función (f(x) o g(x)). Verifique que los valores de 'x' sean válidos en el dominio de la función."

        except SyntaxError:
            return "Error de sintaxis en la función ingresada. Verifique la expresión y asegúrese de que sea válida en Python."

        except NameError:
            return "Error de nombre en la función ingresada: Nombre no definido en la función. Asegúrese de usar la variable 'x' y las funciones de la biblioteca 'math' correctamente."

        except ZeroDivisionError:
            return "Error: División por cero en la función. Asegúrese de que la función no tenga denominadores que se anulen en el intervalo dado."

        except Exception as e:
            return f"Error desconocido: {str(e)}."

        return True
