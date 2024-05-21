"""
1. apply /jobs/<job-id>/<applicant-id> 'allows the applicant apply for a job'
"""
from backend_api.v1.views import kangaroo
from flask import jsonify, abort, render_template, request
from backend_core import applicant


@kangaroo.route('/applicant/new', methods=['GET'], strict_slashes=False)
def create_applicant():
    """
    Sends form for applicant creation
    """
    return render_template('new_applicant.html')


@kangaroo.route('/applicant/new', methods=['POST'], strict_slashes=False)
def create_applicant_new():
    """
    Creates new applicant
    """
    if not request.get_json():
        abort(400)
    applicant_details = request.get_json()
    f_name = applicant_details.get('first_name')
    l_name = applicant_details.get('last_name')
    email = applicant_details.get('email')

    if not f_name or not l_name or not email:
        abort(500)
    try:
        applicantObj = applicant.create_applicant(f_name, l_name, email)
        
        if applicantObj:
            return jsonify({'applicant': applicantObj.to_dict(), 'success': True}), 201
    except Exception:
        return jsonify({'success': False}), 500

@kangaroo.route('/applicant/apply', methods=['POST'], strict_slashes=False)
def applicant_apply_to_job():
    """
    Applies an applicant to a job
    """
    if not request.get_json():
        abort(400)
    job_details = request.get_json()
    applicant_id = job_details.get('applicant_id')
    job_id = job_details.get('job_id')
    
    if not applicant_id or not job_id:
        abort(400)
    if applicant.apply(applicant_id, job_id):
        return jsonify({'success': True}), 201
    return jsonify({'success': False}), 500

@kangaroo.route('/applicant/profile/update', methods=['POST'], strict_slashes=False)
def applicant_update_profile():
    """
    Updates profile of applicant
    """
    if not request.get_json():
        abort(400)
    update_details = request.get_json()
    applicant_id = update_details.get('applicant_id')
    
    if not applicant_id:
        abort(400)
    del update_details['applicant_id']
    
    if applicant.update_profile(applicant_id, **update_details):
        return jsonify({'success': True}), 204
    return jsonify({'success': False}), 500
    