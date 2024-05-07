#!/usr/bin/env python3
"""
Kangaroo API application implementation
"""
from backend_api.v1.views import kangaroo
from flask import Flask


app = Flask(__name__)
app.register_blueprint(kangaroo)


