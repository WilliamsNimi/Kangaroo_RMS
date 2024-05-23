#!/usr/bin/env python3
"""
API endpoint for recruiters
"""
from flask import request, abort, jsonify
from flask import render_template
from backend_api.v1.views import kangaroo
from backend_core import recruiter


@kangaroo.route('/recruiter/jobs/<job_id>', methods=['DELETE'], strict_slashes=False)
def delete_vacancy(job_id):
    """Delete Job from job listings
    
    Keyword arguments:
    @job_id: Id of the Job object to be deleted
    """
    try:
        if not recruiter.delete_job(job_id=job_id):
            return jsonify({'success': False}), 404
        return jsonify({'success': True}), 204
    except Exception as error:
        print(error)
        return jsonify({'success': False}), 204


@kangaroo.route('/recruiter/new', methods=['POST'], strict_slashes=False)
def add_recruiter():
    """
    Adds a recruiter to the db
    """
    if not request.get_json():
        abort(400)
    recruiter_details = request.get_json()
    email = recruiter_details.get('email')
    full_name = recruiter_details.get('full_name')
    
    if not email or not full_name:
        abort(400)
    try:
        recruiterObj = recruiter.create_recruiter(email, full_name)
        
        if recruiterObj:
            del recruiterObj.__dict__["_sa_instance_state"]
            recruiterObj.__dict__['__class__'] = (str(type(recruiterObj)).split('.')[-1]).split('\'')[0]
        return jsonify({'recruiter': recruiterObj.__dict__, 'success': True}), 201
    except Exception as err:
        print(err)
        return jsonify({'success': False}), 409


@kangaroo.route('/recruiter/delete/<recruiter_id>', methods=['DELETE'], strict_slashes=False)
def delete_recruiter(recruiter_id):
    """
    Deletes recruiter from the db
    """
    if not recruiter.find_recruiter(recruiter_id):
        abort(404)

    if recruiter.delete_recruiter(recruiter_id):
        return jsonify({'success': True}), 204
    return jsonify({'success': False}), 400


@kangaroo.route('/recruiter/vacancies/<recruiter_id>', methods=['GET'], strict_slashes=False)
def recruiter_vacancies(recruiter_id):
    """
    Retrieves all vacancies associated with the recruiter
    """
    if not recruiter.find_recruiter(recruiter_id):
        abort(404)
    try:
        vacancy_list = recruiter.recruiter_vacancies(recruiter_id)
    
        if vacancy_list:
            return jsonify({'vacancies': vacancy_list, 'success': True})
        return jsonify({'success': False}), 404
    except Exception as error:
        print(error)
        return jsonify({'success': False}), 400