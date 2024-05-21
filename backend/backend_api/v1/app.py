#!/usr/bin/env python3
"""
Kangaroo API application implementation
"""
from backend_api.v1.views import kangaroo
from flask import Flask, jsonify


app = Flask(__name__)
app.register_blueprint(kangaroo)


@app.errorhandler(404)
def not_found(error):
    """
    Handles NOT FOUND error
    """
    return jsonify({'error': 'Not Found'}), 404

@app.errorhandler(400)
def bad_request(error):
    """
    Handles BAD REQUEST error
    """
    return jsonify({'error': 'Bad Request'}), 400

@app.errorhandler(500)
def server_error(error):
    """
    Handles SERVER ERROR error
    """
    return jsonify({'error': 'Server Error'}), 500

@app.errorhandler(409)
def conflict(error):
    """
    Handles CONFLICT ERROR error
    """
    return jsonify({'error': 'Conflict'}), 409


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)