from flask import *
from flask_cors import CORS

# Define cosntants (btw, HOST='0.0.0.0' <-> listen on all interaces)
HOST = '0.0.0.0'
PORT = 5000
server = Flask(__name__)
CORS(server)

# Routes
@server.route('/', methods=['GET'])
def index():
    return jsonify(message="Hello Wogeagagaerld")

if __name__ == '__main__':
    # Run the server when this file is executed as the main script
    server.run(host=HOST, port=PORT, debug=True)