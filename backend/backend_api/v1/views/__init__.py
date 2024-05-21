#!/usr/bin/env python3
"""
Blueprint for api implementation
"""
from flask import Blueprint

kangaroo = Blueprint('kangaroo', __name__, url_prefix='/kangaroo/v1')

from backend_api.v1.views.applicant import *
from backend_api.v1.views.bp import *
from backend_api.v1.views.recruiter import *

