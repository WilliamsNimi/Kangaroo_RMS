#!/usr/bin/env python3
"""
API endpoint for recruiters
"""
from flask import request, abort, jsonify
from flask import render_template
from backend_api.v1.views import kangaroo


@kangaroo.route('/jobs/requisition-id', methods=['GET'], strict_slashes=False)
def create_job():
    """
    Returns template to create job as required
    """
    job_id = get_requiste_id() # Function to generate new id for job, cached in memory to expire
                               # after a day(or time set) if the job is not created within specified time
    return render_template('requisite_job.html', job_id=job_id)


@kangaroo.route('/jobs/<requisition-id>', methods=['PUT'], strict_slashes=False)
def post_job(requisition_id):
    """
    Creates job to be posted if id exists
    """
    if not request.get_json():
        abort(400)

    job_details = request.get_json()
    job_list = ['requisite_id', 'applicant_id', 'job_id', 'job_title', 'department', 'unit',
                'line_manager', 'number_of_open_positions', 'date_of_requisition', 'business_partner',
                'location', 'job_description', 'job_description_summary', 'recruiter_id']

    if not all(job_details.get(detail) for detail in job_list):
        abort(400)

    if not verify_requisite_id(job_details.get('requisite_id')): # Function to verify whether requisition ID passed with details
        return jsonify({'Error': 'Invalid Requisition ID'}), 404 # exists in cache or in the db - Returns Boolean

    job_created = create_job(job_details) # Returns True if Successful and False Otherwise. It takes a dictionary with neccessary details
                                          # and creates a job to be posted, checks if selected as private and executes accordingly
    if job_created:
        return jsonify({'Successful': True}), 201
    return jsonify({'Successful': False}), 500


@kangaroo.route('/jobs/<job-id>', methods=['DELETE'], strict_slashes=False)
def delete_job(job_id):
    """
    Delete Job from job listings
    """
    if not verify_requisite_id(str(job_id)):
        return jsonify({'Error': 'Invalid Job ID'}), 404
    deleted = delete_from_db_by(job_id=job_id) # Deletes from the db using key, value pairs passed as args and returns True if successful
    
    if deleted:
        return jsonify({'Succesful': True})
    return jsonify({'Succesful': False}), 500



