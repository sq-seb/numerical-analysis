from flask import *
from flask_cors import CORS

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