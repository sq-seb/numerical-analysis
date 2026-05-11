# -----------------------------------------------------
# ADDITIONAL PARSING FOR ONE_VARIABLE ROUTES
import numpy as np
import re

FUNCTION_MAP = {
    "sin": "np.sin",
    "cos": "np.cos",
    "tan": "np.tan",
    "ln": "np.log",
    "log10": "np.log10",
}

CONSTANT_MAP = {
    "e": "np.e",
    "pi": "np.pi",
}

def translate_expr(expr: str) -> str:
    # IMPORTANT: exponent first
    expr = expr.replace("^", "**")

    # functions
    for k, v in FUNCTION_MAP.items():
        expr = re.sub(rf"\b{k}\b", v, expr)

    # constants
    for k, v in CONSTANT_MAP.items():
        expr = re.sub(rf"\b{k}\b", v, expr)

    return expr

def eval_expr(expr: str, x_value: float):
    expr = translate_expr(expr)

    allowed_env = {
        "np": np,
        "x": x_value
    }

    return eval(expr, {"__builtins__": {}}, allowed_env)
# -----------------------------------------------------
import numpy as np
from flask import *
from flask_cors import CORS

from src.one_variable.bisection import bisection

from src.interpolation.vandermonde import vandermonde
from src.interpolation.newton import newton
from src.interpolation.lagrange import lagrange
from src.interpolation.linear_spline import linear_spline
from src.interpolation.quadratic_spline import quadratic_spline
from src.interpolation.cubic_spline import cubic_spline

# Define constants
HOST = '0.0.0.0'
PORT = 5000

server = Flask(__name__)
CORS(server)

# ==================================================================
# ONE VARIABLE ROUTES
@server.route('/bisection', methods=['POST'])
def bisection_route():
    data = request.get_json()

    f_str = data.get("f")
    a = float(data.get("a"))
    b = float(data.get("b"))
    niter = int(data.get("niter"))
    value = float(data.get("value"))
    tol_type = data.get("tol_type")

    print("raw:", f_str)

    # 1. Translate to numpy syntax
    safe_expr = translate_expr(f_str)
    print("translated:", safe_expr)

    # 2. Build safe function f(x)
    def f(x):
        return eval_expr(f_str, x)

    # 3. Run bisection
    result = bisection(
        f=f,
        a=a,
        b=b,
        niter=niter,
        value=value,
        tol_type=tol_type
    )
    print(result)
    return jsonify(result)

# ==================================================================
# INTERPOLATION ROUTES
@server.route('/vandermonde', methods=['GET', 'POST'])
def vandermonde_route():
    data = request.get_json()

    validation_percent = float(data.get("validationPercent"))
    pairs = data.get("pairs")

    result = vandermonde(validation_percent, pairs)

    return jsonify(result)

@server.route('/newton', methods=['GET', 'POST'])
def newton_route():
    data = request.get_json()

    validation_percent = float(data.get("validationPercent"))
    pairs = data.get("pairs")

    result = newton(validation_percent, pairs)

    return jsonify(result)

@server.route('/lagrange', methods=['GET', 'POST'])
def lagrange_route():
    data = request.get_json()

    validation_percent = float(data.get("validationPercent"))
    pairs = data.get("pairs")

    result = lagrange(validation_percent, pairs)

    return jsonify(result)

@server.route('/linear_spline', methods=['GET', 'POST'])
def linear_spline_route():
    data = request.get_json()

    validation_percent = float(data.get("validationPercent"))
    pairs = data.get("pairs")

    result = linear_spline(validation_percent, pairs)

    return jsonify(result)

@server.route('/quadratic_spline', methods=['GET', 'POST'])
def quadratic_spline_route():
    data = request.get_json()

    validation_percent = float(data.get("validationPercent"))
    pairs = data.get("pairs")

    result = quadratic_spline(validation_percent, pairs)

    return jsonify(result)

@server.route('/cubic_spline', methods=['GET', 'POST'])
def cubic_spline_route():
    data = request.get_json()

    validation_percent = float(data.get("validationPercent"))
    pairs = data.get("pairs")

    result = cubic_spline(validation_percent, pairs)

    return jsonify(result)
# ==================================================================

if __name__ == '__main__':
    server.run(host=HOST, port=PORT, debug=True)