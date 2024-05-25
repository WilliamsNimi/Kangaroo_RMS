"""
1. apply /jobs/<job-id>/<applicant-id> 'allows the applicant apply for a job'
"""
from backend_api.v1.views import kangaroo
from flask import jsonify, abort, render_template, request, make_response
from flask import g, url_for, redirect
from backend_core import applicant
from backend_auth import applicant_auth, session_auth


@kangaroo.route('/applicant/home', methods=['GET'], strict_slashes=False)
def applicant_home():
    """
    Home page of applicant
    """
    return jsonify({'success': True, 'message': 'Welcome Home APPLICANT!'})


@kangaroo.route('/applicant/login', methods=['GET'], strict_slashes=False)
def applicant_login_get():
    """
    Applicant login
    """
    session_token = request.cookies.get('session_token')
    if session_token:
        applicant_details = session_auth.verify_session(session_token)
        if applicant_details:
            setattr(g, applicant_details[0], applicant_details[1])
            return redirect(url_for('kangaroo.applicant_home'))
    return jsonify({'success': True, 'message': 'This is the Applicant login page'})


@kangaroo.route('/applicant/login', methods=['POST'], strict_slashes=False)
def applicant_login_post():
    """
    Applicant login
    """
    try:
        # applicant_dict = request.form.to_dict()
        applicant_dict = request.get_json()
        if applicant_dict:
            applicant_details = applicant_auth.verify_credentials(**applicant_dict)
            if applicant_details:
                setattr(g, applicant_details[0], applicant_details[1])
                response = make_response(redirect(url_for('kangaroo.applicant_home')))        
                session_token = session_auth.create_session('applicant', applicant_details[1])
                response.set_cookie(
                    'session_token',
                    str(session_token),
                    httponly=True,
                    secure=False
                    # samesite='Lax'
                )
                return response
        return redirect(url_for('kangaroo.applicant_login_get'))
    except Exception as error:
        print(error)
        return redirect(url_for('kangaroo.applicant_login_get'))


@kangaroo.route('/applicant/logout', methods=['POST'], strict_slashes=False)
def applicant_logout():
    """
    Logs out currently logged in user
    """
    from backend_api.v1.app import app

    session_token = request.cookies.get('session_token')
    if session_token:
        session_auth.delete_session(session_token)
        return redirect(url_for('home'))
    return jsonify({'error': 'session token not found'}), 404


@kangaroo.route('/applicant/signup', methods=['GET'], strict_slashes=False)
def create_applicant():
    """
    Sends form for applicant creation
    """
    return render_template('new_applicant.html')


@kangaroo.route('/applicant/signup', methods=['POST'], strict_slashes=False)
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
    password = applicant_details.get('password')

    if not f_name or not l_name or not email or not password:
        abort(400)
    try:
        applicantObj = applicant.create_applicant(f_name, l_name, email, password)
        if applicantObj:
            del applicantObj.__dict__["_sa_instance_state"]
            del applicantObj.__dict__["password"]
            applicantObj.__dict__['__class__'] = (str(type(applicantObj)).split('.')[-1]).split('\'')[0]
            return jsonify({'applicant': applicantObj.__dict__, 'success': True}), 201
    except Exception as err:
        print(err)
        return jsonify({'success': False, 'message': err}), 500


@kangaroo.route('/applicant/profile/update', methods=['PUT'], strict_slashes=False)
def applicant_update_profile():
    """
    Updates profile of applicant
    """
    if not request.get_json():
        abort(400)
    update_details = request.get_json()
    update_details.pop('applicant_id', None)
    update_details.pop('id', None)
    applicant_id = g.applicant_id

    if not applicant_id:
        abort(400)
    try:
        if applicant.update_profile(applicant_id, **update_details):
            return jsonify({'success': True})
        return jsonify({'success': False}), 500
    except Exception as error:
        print(error)
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
    try:
        if applicant.apply(applicant_id, job_id):
            return jsonify({'success': True}), 201
        return jsonify({'success': False}), 500
    except Exception as error:
        print(error)
        return jsonify({'success': False}), 500
    