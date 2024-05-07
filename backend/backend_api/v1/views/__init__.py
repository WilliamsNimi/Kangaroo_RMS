#!/usr/bin/env python3
"""
Blueprint for api implementation
"""
from flask import Blueprint

kangaroo = Blueprint('kangaroo', __name__, url_prefix='/kangaroo/v1')
