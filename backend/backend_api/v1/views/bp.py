#!/usr/bin/env python3
""" 
1. make_requisition /requisitions POST 'makes a vacancy request to the recruiter'
"""
from backend_api.v1.views import kangaroo
from flask import request, abort, render_template, jsonify
from backend_core import bp



@kangaroo.route('/bp/requisitions', methods=['GET'], strict_slashes=False)
def bp_create_requisition():
    """
    Returns template to create vacancy requisition
    """
    return render_template('new_requisition.html')


@kangaroo.route('/bp/requisitions', methods=['POST'], strict_slashes=False)
def bp_post_vacancy():
    """
    Creates job to be posted if requisition-id exists
    """
    if not request.get_json():
        abort(400)
    vacancy_details = request.get_json()
    vacancy_list = ['job_title', 'department', 'unit',
                'line_manager', 'number_of_open_positions',
                'location', 'job_description_summary', 'recruiter_id']
    if not all(vacancy_details.get(detail) for detail in vacancy_list):
        abort(400)

    job_title = vacancy_details.get('job_title')
    department = vacancy_details.get('department')
    unit = vacancy_details.get('unit')
    line_manager = vacancy_details.get('line_manager')
    number_of_open_positions = vacancy_details.get('number_of_open_positions')
    location = vacancy_details.get('location')
    job_description_summary = vacancy_details.get('job_description_summary')
    recruiter_id = vacancy_details.get('recruiter_id') # Should we not be expecting a recruiter_id?
    
    vacancy_created = bp.make_requisition(job_title, department, unit, line_manager,
                                          number_of_open_positions, location, job_description_summary) 
    if vacancy_created:
        return jsonify({'success': True, 'vacancy': vacancy_created.to_dict()}), 201
    return jsonify({'success': False}), 500

@kangaroo.route('/bp/profile/update', methods=['POST'], strict_slashes=False)
def bp_update_profile():
    """
    Updates profile of the business partner
    """
    if not request.get_json():
        abort(400)
    update_details = request.get_json()
    email = update_details.get('email')
    
    if not email:
        abort(404)
    if bp.update_profile(email, **update_details):
        return jsonify({'success': True}), 204
    return jsonify({'success': False}), 500

@kangaroo.route('/bp/profile/delete', methods=['DELETE'], strict_slashes=False)
def bp_delete():
    """
    Deletes BP object from the database
    """
    if not request.get_json():
        abort(400)
    bp_details = request.get_json()
    email = bp_details.get('email')
    # T.B.I === TO BE IMPLEMENTED
    if not email:
        abort(404)
    if not bp.find_business_partner_by(email): # Check if bp exists - TBI
        abort(404)
    success = bp.delete_business_partner(email=email) # Delete business partner - TBI
    
    if success:
        return jsonify({'success': True}), 204
    return jsonify({'success': False}), 500 
    
    
