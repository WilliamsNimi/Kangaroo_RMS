"""
API endpoint for recruiters
"""
from flask import request, abort, jsonify, g, redirect, url_for
from flask import render_template, make_response
from backend_core import recruiter
from backend_auth import recruiter_auth, session_auth
from flask import Blueprint


# Defining a blueprint
recruiter_bp = Blueprint(
    'recruiter_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@recruiter_bp.route('/recruiter/home', methods=['GET'], strict_slashes=False)
def recruiter_home():
    """
    Home page of recruiter
    jsonify({'success': True, 'message': 'Welcome Home RECRUITER!'})
    """
    return render_template("recruiter/SignIn.html")


@recruiter_bp.route('/recruiter/login', methods=['GET'], strict_slashes=False)
def recruiter_login_get():
    """
    Recruiter login
    """
    session_token = request.cookies.get('session_token')
    if session_token:
        recruiter_details = session_auth.verify_session(session_token)
        if recruiter_details:
            setattr(g, recruiter_details[0], recruiter_details[1])
            return redirect(url_for('kangaroo.recruiter_home'))
    return jsonify({'success': True, 'message': 'This is the Recruiter login page'})


@recruiter_bp.route('/recruiter/login', methods=['POST'], strict_slashes=False)
def recruiter_login_post():
    """
    Recruiter login
    """
    try:
        recruiter_dict = request.form.to_dict()
        if recruiter_dict:
            recruiter_details = recruiter_auth.verify_credentials(**recruiter_dict)
            if recruiter_details:
                setattr(g, recruiter_details[0], recruiter_details[1])
                response = make_response(redirect(url_for('kangaroo.recruiter_home')))
                session_token = session_auth.create_session('recruiter', recruiter_details[1])
                response.set_cookie(
                    'session_token', 
                    str(session_token), 
                    httponly=True, 
                    secure=False,
                    path='/kangaroo/v1/recruiter'
                    # samesite='Lax'
                )
                return response
        return redirect(url_for('kangaroo.recruiter_login_get'))
    except Exception as error:
        print(error)
        return redirect(url_for('kangaroo.recruiter_login_get'))


@recruiter_bp.route('/recruiter/logout', methods=['POST'], strict_slashes=False)
def recruiter_logout():
    """
    Logs out currently logged in user
    """
    from backend_api.v1.app import app

    session_token = request.cookies.get('session_token')
    if session_token:
        session_auth.delete_session(session_token)
        return redirect(url_for('home'))
    return jsonify({'error': 'session token not found'}), 404


@recruiter_bp.route('/recruiter/signup', methods=['GET'], strict_slashes=False)
def create_recruiter():
    """
    Sends form for recruiter creation
    """
    return render_template('new_recruiter.html')


@recruiter_bp.route('/recruiter/signup', methods=['POST'], strict_slashes=False)
def add_recruiter():
    """
    Adds a recruiter to the db
    """
    if not request.form.to_dict():
        abort(400)
    recruiter_details = request.form.to_dict()
    email = recruiter_details.get('email')
    full_name = recruiter_details.get('full_name')
    password = recruiter_details.get('password')
    
    if not email or not password or not full_name:
        abort(400)
    try:
        recruiterObj = recruiter.create_recruiter(email, full_name, password)
        
        if recruiterObj:
            return redirect(url_for('kangaroo.recruiter_login_get'))
        return jsonify({'success': False}), 409
    except Exception as err:
        print(err)
        return jsonify({'success': False}), 409


@recruiter_bp.route('/recruiter/profile/update', methods=['PUT'], strict_slashes=False)
def recruiter_update_profile():
    """
    Updates profile of recruiter
    """
    if not request.form.to_dict():
        abort(400)
    update_details = request.form.to_dict()
    update_details.pop('recruiter_id', None)
    update_details.pop('id', None)
    update_details.pop('email', None)
    recruiter_id = g.recruiter_id

    if not recruiter_id:
        abort(400)
    try:
        if recruiter.update_profile(recruiter_id, **update_details):
            if 'password' in update_details:
                session_token = request.cookies.get('session_token')
                session_auth.delete_session(session_token)
                return redirect(url_for('kangaroo.recruiter_login_get'))
            return jsonify({'success': True})
        return jsonify({'success': False}), 500
    except Exception as error:
        print(error)
        return jsonify({'success': False}), 500


@recruiter_bp.route('/recruiter/delete/<recruiter_id>', methods=['DELETE'], strict_slashes=False)
def delete_recruiter(recruiter_id):
    """
    Deletes recruiter from the db
    """
    if not recruiter.find_recruiter(recruiter_id):
        abort(404)
    if recruiter.delete_recruiter(recruiter_id):
        return jsonify({'success': True}), 204
    return jsonify({'success': False}), 400


@recruiter_bp.route('/recruiter/vacancies/<recruiter_id>', methods=['GET'], strict_slashes=False)
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


@recruiter_bp.route('/recruiter/jobs/<job_id>', methods=['DELETE'], strict_slashes=False)
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