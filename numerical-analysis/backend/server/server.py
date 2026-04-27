from flask import Flask, jsonify, request
from flask_cors import CORS
from numerical.services.bisection_service import BisectionService
from numerical.services.secant_service import SecantService
from numerical.services.regula_falsi_service import RegulaFalsiService
from numerical.services.newton_service import NewtonService
from numerical.services.fixed_point_service import FixedPointService
from numerical.services.multiple_roots_2_service import MultipleRoots2Service

# Define constants
HOST = '0.0.0.0'
PORT = 5000
server = Flask(__name__)
CORS(server)

# Initialize services
bisection_service = BisectionService()
secant_service = SecantService()
regula_falsi_service = RegulaFalsiService()
newton_service = NewtonService()
fixed_point_service = FixedPointService()
multiple_roots_2_service = MultipleRoots2Service()

# Routes
@server.route('/', methods=['GET'])
def index():
    return jsonify(message="API de Métodos Numéricos - Análisis Numérico")

@server.route('/api/bisection', methods=['POST'])
def bisection():
    try:
        data = request.json
        function_f = data.get('function_f')
        interval_a = float(data.get('interval_a'))
        interval_b = float(data.get('interval_b'))
        tolerance = float(data.get('tolerance'))
        max_iterations = int(data.get('max_iterations'))
        precision = data.get('precision', False)
        
        validation = bisection_service.validate_input(
            interval_a, interval_b, tolerance, max_iterations, function_f
        )
        
        if validation is not True:
            return jsonify({"error": validation}), 400
            
        result = bisection_service.solve(
            function_f, interval_a, interval_b, tolerance, max_iterations, precision
        )
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route('/api/secant', methods=['POST'])
def secant():
    try:
        data = request.json
        function_f = data.get('function_f')
        x0 = float(data.get('x0'))
        interval_b = float(data.get('interval_b'))
        tolerance = float(data.get('tolerance'))
        max_iterations = int(data.get('max_iterations'))
        precision = data.get('precision', False)
        
        validation = secant_service.validate_input(
            x0, tolerance, max_iterations, function_f, interval_b=interval_b
        )
        
        if validation is not True:
            return jsonify({"error": validation}), 400
            
        result = secant_service.solve(
            function_f, x0, tolerance, max_iterations, precision, interval_b=interval_b
        )
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route('/api/regula-falsi', methods=['POST'])
def regula_falsi():
    try:
        data = request.json
        function_f = data.get('function_f')
        interval_a = float(data.get('interval_a'))
        interval_b = float(data.get('interval_b'))
        tolerance = float(data.get('tolerance'))
        max_iterations = int(data.get('max_iterations'))
        precision = data.get('precision', False)
        
        validation = regula_falsi_service.validate_input(
            function_f, interval_a, interval_b, tolerance, max_iterations
        )
        
        if validation is not True:
            return jsonify({"error": validation}), 400
            
        result = regula_falsi_service.solve(
            function_f, interval_a, interval_b, tolerance, max_iterations, precision
        )
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route('/api/newton', methods=['POST'])
def newton():
    try:
        data = request.json
        function_f = data.get('function_f')
        x0 = float(data.get('x0'))
        tolerance = float(data.get('tolerance'))
        max_iterations = int(data.get('max_iterations'))
        precision = data.get('precision', False)
        
        validation = newton_service.validate_input(
            x0, tolerance, max_iterations, function_f
        )
        
        if validation is not True:
            return jsonify({"error": validation}), 400
            
        result = newton_service.solve(
            function_f, x0, tolerance, max_iterations, precision
        )
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route('/api/fixed-point', methods=['POST'])
def fixed_point():
    try:
        data = request.json
        function_f = data.get('function_f')
        function_g = data.get('function_g')
        x0 = float(data.get('x0'))
        tolerance = float(data.get('tolerance'))
        max_iterations = int(data.get('max_iterations'))
        precision = data.get('precision', False)
        
        validation = fixed_point_service.validate_input(
            x0, tolerance, max_iterations, function_f, function_g=function_g
        )
        
        if validation is not True:
            return jsonify({"error": validation}), 400
            
        result = fixed_point_service.solve(
            function_f, function_g, x0, tolerance, max_iterations, precision
        )
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route('/api/multiple-roots-2', methods=['POST'])
def multiple_roots_2():
    try:
        data = request.json
        function_f = data.get('function_f')
        x0 = float(data.get('x0'))
        tolerance = float(data.get('tolerance'))
        max_iterations = int(data.get('max_iterations'))
        precision = data.get('precision', False)
        
        validation = multiple_roots_2_service.validate_input(
            x0, tolerance, max_iterations, function_f
        )
        
        if validation is not True:
            return jsonify({"error": validation}), 400
            
        result = multiple_roots_2_service.solve(
            x0=x0, tolerance=tolerance, max_iterations=max_iterations,
            precision=precision, function_f=function_f
        )
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the server when this file is executed as the main script
    server.run(host=HOST, port=PORT, debug=True)