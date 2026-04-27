import sympy as sp
import math
from numerical.interfaces.iterative_method import IterativeMethod
from shared.utils.convert_math_to_simply import convert_math_to_sympy
from shared.utils.plot_function import plot_function

class NewtonService(IterativeMethod):

    def solve(
        self,
        function_f: str,
        x0: float,
        tolerance: float,
        max_iterations: int,
        precision: bool = False,
        **kwargs,
    ) -> dict:
        try:
            if isinstance(x0, str):
                x0 = float(x0.replace(",", "."))
            if isinstance(tolerance, str):
                tolerance = float(tolerance.replace(",", "."))
        except ValueError:
            return self._prepare_response(
                message="x0 y tolerancia deben ser números válidos.",
                table={},
                is_successful=False,
                have_solution=False,
                points=[(0, 0)],
                function=function_f,
                warnings=[]
            )

        x = sp.symbols("x")
        sympy_function_f = convert_math_to_sympy(function_f)
        f_expr = sp.sympify(sympy_function_f)
        f_prime_expr = sp.diff(f_expr, x)
        f = sp.lambdify(x, f_expr, modules=["math"])
        f_prime = sp.lambdify(x, f_prime_expr, modules=["math"])

        table = {}
        x0_current = float(x0)
        current_error = math.inf
        current_iteration = 1
        points = [(x0_current, 0)]
        warnings = []

        history = [x0_current]

        while current_iteration <= max_iterations:
            try:
                fx = f(x0_current)
                f_prime_x = f_prime(x0_current)

                if abs(f_prime_x) < 1e-10:
                    warnings.append(f"f'(x) ≈ 0 en x = {x0_current:.8g}. El método puede divergir o devolver valores erróneos.")
                    return self._prepare_response(
                        message=f"Error: La derivada es cero o muy cercana a cero en x = {x0_current:.8g}. No se puede continuar.",
                        table=table,
                        is_successful=False,
                        have_solution=False,
                        points=points,
                        function=function_f,
                        warnings=warnings
                    )
                x_next = x0_current - fx / f_prime_x

            except Exception as e:
                return self._prepare_response(
                    message=f"Error al evaluar la función o su derivada: {str(e)}.",
                    table=table,
                    is_successful=False,
                    have_solution=False,
                    points=points,
                    function=function_f,
                    warnings=warnings
                )

            error_value = (
                abs(x_next - x0_current) if precision
                else abs((x_next - x0_current) / x_next) if x_next != 0 else abs(x_next - x0_current)
            )

            table[current_iteration] = {
                "iteration": current_iteration,
                "approximate_value": x0_current,
                "f_evaluated": fx,
                "f_prime_evaluated": f_prime_x,
                "next_x": x_next,
                "error": error_value,
            }
            points.append((x0_current, fx))
            history.append(x_next)

            if current_iteration > 2 and abs(history[-1] - history[-3]) < tolerance:
                warnings.append("El método parece estar oscilando entre dos valores. Puede que no converja.")

            if abs(x_next) > 1e16 or math.isnan(x_next):
                warnings.append("Error: El valor de x creció demasiado (divergencia detectada).")
                return self._prepare_response(
                    message="Error: El método está divergiendo (|x| > 1e16 o NaN).",
                    table=table,
                    is_successful=False,
                    have_solution=False,
                    points=points,
                    function=function_f,
                    warnings=warnings
                )

            if fx == 0 or error_value < tolerance:
                msg = f"{x_next} es una aproximación de la raíz de f(x) con error menor a {tolerance}."
                return self._prepare_response(
                    message=msg,
                    table=table,
                    is_successful=True,
                    have_solution=True,
                    points=points,
                    function=function_f,
                    warnings=warnings
                )

            x0_current = x_next
            current_iteration += 1

        msg = f"El método funcionó pero no se encontró solución en {max_iterations} iteraciones."
        return self._prepare_response(
            message=msg,
            table=table,
            is_successful=False,
            have_solution=False,
            points=points,
            function=function_f,
            warnings=warnings
        )

    def _prepare_response(
        self,
        message: str,
        table: dict,
        is_successful: bool,
        have_solution: bool,
        points: list,
        function: str,
        warnings=None,
    ) -> dict:
        plot_function(
            function_f=function,
            have_solution=have_solution,
            points=points,
        )
        return {
            "message_method": message,
            "table": table,
            "is_successful": is_successful,
            "have_solution": have_solution,
            "root": points[-1][0] if have_solution else 0.0,
            "warnings": warnings if warnings else [],
        }

    def validate_input(
        self,
        x0: float | str,
        tolerance: float | str,
        max_iterations: int,
        function_f: str,
        **kwargs,
    ) -> str | bool:

        try:
            if isinstance(x0, str):
                x0 = float(x0.replace(",", "."))
            else:
                x0 = float(x0)
            if isinstance(tolerance, str):
                tolerance = float(tolerance.replace(",", "."))
            else:
                tolerance = float(tolerance)
        except ValueError:
            return "x0 y tolerancia deben ser números reales válidos."

        if tolerance <= 0:
            return "La tolerancia debe ser un número positivo"
        if not isinstance(max_iterations, int) or max_iterations <= 0:
            return "El máximo número de iteraciones debe ser un entero positivo."
        
        try:
            x = sp.symbols("x")
            sympy_function_f = convert_math_to_sympy(function_f)
            f_expr = sp.sympify(sympy_function_f)
            if f_expr.free_symbols != {x}:
                return "Error al interpretar la función: utilice la variable 'x'."
            sp.diff(f_expr, x)
        except Exception as e:
            return f"Error al interpretar la función ingresada: {str(e)}."
        return True
