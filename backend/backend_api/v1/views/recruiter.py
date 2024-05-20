#!/usr/bin/env python3
"""
API endpoint for recruiters
"""
from flask import request, abort, jsonify
from flask import render_template
from backend_api.v1.views import kangaroo
from backend.recruiter import Recruiter

"""
1. post_job /jobs/<job-id> POST 'posting a job so it is visible to the applicants'
2. delete_job /jobs/<job-id> 'delete a job so it is not visible to applicants'
3. search_candidateDB /applicants/search?query="" 'search the applicant table for relevant data'
"""


@kangaroo.route('/applicants/search', methods=['GET'], strict_slashes=False)
def applicant_bool_search():
    """Search for an applicant using a bool search
    """
    bool_details = request.args.to_dict()
    applicants = Recruiter.boolean_search(**bool_details)
    
    if not applicants:
        return jsonify({'success': False}), 404
    return jsonify({'success': True, 'applicants': applicants})
    

@kangaroo.route('/jobs/<job-id>', methods=['DELETE'], strict_slashes=False)
def delete_vacancy(job_id):
    """Delete Job from job listings
    
    Keyword arguments:
    @job_id: Id of the Job object to be deleted
    """
    if not Recruiter.delete_job(job_id=job_id):
        return jsonify({'success': False}), 404
    return jsonify({'success': True}), 204
        

@kangaroo.route('/recruiter/applicants/<recruiter-id>', methods=['GET'], strict_slashes=False)
def recruiter_applicants

