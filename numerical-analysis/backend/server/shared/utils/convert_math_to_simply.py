import math
import re

MATH_FUNCTIONS = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "sinh": math.sinh,
    "cosh": math.cosh,
    "tanh": math.tanh,
    "asinh": math.asinh,
    "acosh": math.acosh,
    "atanh": math.atanh,
    "exp": math.exp,
    "log": math.log,
    "sqrt": math.sqrt,
    "abs": abs,
    "fabs": math.fabs,
    "floor": math.floor,
    "ceil": math.ceil,
    "round": round,
}

MATH_CONSTANTS = {
    "e": math.e,
    "E": math.e,
    "pi": math.pi,
    "tau": math.tau,
}


def normalize_math_expression(function_f: str) -> str:
    """Normalize an expression for Python eval and math module evaluation."""
    expression = function_f.strip()
    expression = expression.replace("^", "**")
    expression = re.sub(r"\bln\b", "log", expression)
    expression = re.sub(r"\bsen\b", "sin", expression)
    return expression


def get_math_eval_context() -> dict:
    return {**MATH_FUNCTIONS, **MATH_CONSTANTS, "math": math}


def get_safe_eval_globals() -> dict:
    return {"__builtins__": None, **get_math_eval_context()}


def convert_math_to_sympy(function_f: str) -> str:
    """
    Convert math function notation to sympy-compatible notation.
    Replaces common math functions with their sympy equivalents.
    """
    expression = function_f.strip()
    expression = expression.replace("^", "**")
    expression = re.sub(r"\bln\b", "log", expression)
    expression = re.sub(r"\bsen\b", "sin", expression)
    expression = re.sub(r"\be\b", "E", expression)

    return expression
