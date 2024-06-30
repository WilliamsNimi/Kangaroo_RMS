"""
TODO:
        1. Applicants should be able to apply.
        2. Applicants should be able to search for vacancies.
        3. Applicants should be able to see list of vacancies they applied for.
GLOBAL: 
        1. Implement password Regex.
        2. Implement SQL injection checks for all forms.
        3. Implement Session Management for Logout.
"""
from flask import Blueprint
from flask import jsonify, abort, render_template, request, make_response
from flask import g, url_for, redirect
from backend_core import applicant
from backend_auth import applicant_auth, session_auth
import bcrypt

email_ = ""
firstName = ""
lastName = ""
message = ""

# Defining a blueprint
applicant_bp = Blueprint(
    'applicant_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@applicant_bp.route('/applicant/home', methods=['GET'], strict_slashes=False)
def applicant_home():
    """
    Signup page of applicant
    """
    return render_template("applicant/Signup.html", message=message)

@applicant_bp.route('/applicant/homepage', methods=['GET'], strict_slashes=False)
def applicant_homepage():
    """
    Home page of applicant
    """
    return render_template("applicant/Home.html")

@applicant_bp.route('/jobs', methods=['GET'], strict_slashes=False)
def applicant_get_jobs():
    """
    Home page of applicant
    """
    return render_template("applicant/Job.html")

@applicant_bp.route('/applicant/profile', methods=['GET'], strict_slashes=False)
def applicant_profile():
    """
    Get Profile page of Applicant
    """
    return render_template("applicant/Profile.html", email=email_, first_name=firstName, last_name=lastName)

@applicant_bp.route('/applicant/forgot_password', methods=['GET'], strict_slashes=False)
def applicant_forgot_password():
    """
    TODO: Build this function properly
    resets applicant password
    """
    return render_template("applicant/PasswordRecovery.html")

@applicant_bp.route('/applicant/login', methods=['GET'], strict_slashes=False)
def applicant_login_get():
    """
    Applicant login
    """
    session_token = request.cookies.get('session_token')
    if session_token:
        applicant_details = session_auth.verify_session(session_token)
        if applicant_details:
            setattr(g, applicant_details[0], applicant_details[1])
            return redirect(url_for('applicant_bp.applicant_home'))
    return render_template("applicant/SignIn.html")


@applicant_bp.route('/applicant/login', methods=['POST'], strict_slashes=False)
def applicant_login_post():
    """
    Applicant login
     """
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        applicant_= applicant.find_applicant(email)
        global email_
        global firstName
        global lastName
        try:
            email_ = applicant_.email
            firstName = applicant_.first_name
            lastName = applicant_.last_name
            print(applicant_.password)
            p_bytes = password.encode('utf-8')
            hashed_password_val = bcrypt.checkpw(p_bytes, applicant_.password)
            if hashed_password_val and email == applicant_.email:
                return render_template("applicant/Home.html", email=email_, first_name=firstName, last_name=lastName)
        except Exception:
            error_message =  "Username or Password incorrect"
    return render_template("applicant/SignIn.html", error_message=error_message)


@applicant_bp.route('/applicant/logout', methods=['POST'], strict_slashes=False)
def applicant_logout():
    """
    Logs out currently logged in user
    """
    from backend_api.v1.app import app

    try:
        session_token = request.cookies.get('session_token')
        if session_token:
            session_auth.delete_session(session_token)
            return redirect(url_for('home'))
        return jsonify({'error': 'session token not found'}), 404
    except Exception as error:
        print(error)
        return jsonify({'error': 'session token not found'}), 404


@applicant_bp.route('/applicant/signup', methods=['GET'], strict_slashes=False)
def create_applicant():
    """
    Sends form for applicant creation
    """
    return render_template('new_applicant.html')


@applicant_bp.route('/applicant/signup', methods=['POST'], strict_slashes=False)
def create_applicant_new():
    """
    Creates new applicant
    """
    global message
    if not request.form.to_dict():
        message = "Please fill the details in the form"
        return redirect(url_for('applicant_bp.applicant_home', message=message))

    applicant_details = request.form.to_dict()
    f_name = applicant_details.get('first_name')
    l_name = applicant_details.get('last_name')
    email = applicant_details.get('email')
    password = applicant_details.get('password')

    if not f_name or not l_name or not email or not password:
        message = "Please fill the details in the form"
        return redirect(url_for('applicant_bp.applicant_home', message=message))
    try:
        applicantObj = applicant.create_applicant(f_name, l_name, email, password)
        
        if applicantObj:
            return redirect(url_for('applicant_bp.applicant_login_get'))
        return jsonify({'success': False})
    except Exception as e:
        message = "Applicant with " + email + " already exists. Please click on forgot password."
        return redirect(url_for('applicant_bp.applicant_home', message=message))

@applicant_bp.route('/applicant/profile/update', methods=['PUT'], strict_slashes=False)
def applicant_update_profile():
    """
    Updates profile of applicant
    """
    if not request.form.to_dict():
        abort(400)
    update_details = request.form.to_dict()
    update_details.pop('applicant_id', None)
    update_details.pop('id', None)
    update_details.pop('email', None)
    applicant_id = g.applicant_id

    if not applicant_id:
        abort(400)
    try:
        if applicant.update_profile(applicant_id, **update_details):
            if 'password' in update_details:
                session_token = request.cookies.get('session_token')
                session_auth.delete_session(session_token)
                return redirect(url_for('kangaroo.applicant_login_get'))
            return jsonify({'success': True})
        return jsonify({'success': False}), 500
    except Exception as error:
        print(error)
        return jsonify({'success': False}), 500


@applicant_bp.route('/applicant/apply', methods=['GET', 'POST'], strict_slashes=False)
def applicant_apply_to_job():
    """
    Applies an applicant to a job
    """
    if request.method == 'GET':
        return render_template('applicant/Job.HTML')
    if not request.form.to_dict():
        abort(400)
    job_details = request.form.to_dict()
    applicant_id = g.applicant_id
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
    