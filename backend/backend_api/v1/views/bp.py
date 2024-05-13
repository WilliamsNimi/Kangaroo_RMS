#!/usr/bin/env python3
""" 
1. make_requisition /requisitions POST 'makes a vacancy request to the recruiter'
"""
from backend.backend_api.v1.views import kangaroo
from flask import request, abort, render_template, jsonify
from backend.bp import BusinessPartner



@kangaroo.route('/requisitions', methods=['GET'], strict_slashes=False)
def create_requisition():
    """
    Returns template to create vacancy requisition
    """
    return render_template('new_requisition.html')


@kangaroo.route('/requisitions', methods=['POST'], strict_slashes=False)
def post_vacancy(requisition_id):
    """
    Creates job to be posted if requisition-id exists
    """
    if not request.get_json():
        abort(400)
    vacancy_details = request.get_json()
    vacancy_list = ['job_id', 'job_title', 'department', 'unit',
                'line_manager', 'number_of_open_positions', 'date_of_requisition',
                'location', 'job_description', 'job_description_summary', 'recruiter_id']

    if not all(vacancy_details.get(detail) for detail in vacancy_list):
        abort(400)
    vacancy_created = BusinessPartner.make_requisition(vacancy_details) 
    if vacancy_created:
        return jsonify({'success': True, 'vacancy': vacancy_created}), 201
    return jsonify({'success': False}), 500