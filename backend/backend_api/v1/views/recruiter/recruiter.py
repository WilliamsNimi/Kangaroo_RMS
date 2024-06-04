"""
API endpoint for recruiters
"""
from flask import request, abort, jsonify, g, redirect, url_for, flash
from flask import render_template, make_response
from backend_core import recruiter
from backend_auth import recruiter_auth, session_auth
from flask import Blueprint
import bcrypt

email_ = ""
fullName = ""

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
    return render_template("recruiter/Signup.html")

@recruiter_bp.route('/recruiter/homepage', methods=['GET'], strict_slashes=False)
def recruiter_homepage():
    """
    TODO: Build a solid redirect
    Home page of recruiter
    """
    jobs = recruiter.show_all_vacancies()
    return render_template("recruiter/Home.html", full_name=fullName, email=email_, jobs=jobs)


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
            return render_template("recruiter/Home.html", full_name=fullName, email=email_)
    return render_template("recruiter/SignIn.html")


@recruiter_bp.route('/recruiter/login', methods=['POST'], strict_slashes=False)
def recruiter_login_post():
    """
    Recruiter login
    
    try:
        recruiter_dict = request.form.to_dict()
        if recruiter_dict:
            recruiter_details = recruiter_auth.verify_credentials(**recruiter_dict)
            if recruiter_details:
                setattr(g, recruiter_details[0], recruiter_details[1])
                response = make_response(redirect(url_for('recruiter_bp.recruiter_homepage')))
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
        return redirect(url_for('recruiter_bp.recruiter_homepage'))
    except Exception as error:
        print(error)
        return redirect(url_for('recruiter_bp.recruiter_login_get')) """
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        recruiter_= recruiter.find_recruiter_by(email)
        global email_
        global fullName
        email_ = recruiter_.email
        fullName = recruiter_.full_name
        p_bytes = password.encode('utf-8')
        hashed_password_val = bcrypt.checkpw(p_bytes, recruiter_.password)
        if hashed_password_val and email == recruiter_.email:
            return redirect(url_for("recruiter_bp.recruiter_homepage", full_name=recruiter_.full_name, email=recruiter_.email))
    return render_template("recruiter/SignIn.html")

@recruiter_bp.route('/recruiter/logout', methods=['GET', 'POST'], strict_slashes=False)
def recruiter_logout():
    """
    Logs out currently logged in user
    """
    from app import app

    session_token = request.cookies.get('session_token')
    if session_token:
        session_auth.delete_session(session_token)
        return render_template("recruiter/SignIn.html")
    return jsonify({'error': 'session token not found'}), 404


@recruiter_bp.route('/recruiter/newRecruiter', methods=['GET'], strict_slashes=False)
def create_recruiter():
    """
    Sends form for recruiter creation
    """
    return render_template('recruiter/newRecruiter.html', full_name=fullName, email=email_)

@recruiter_bp.route('/recruiter/create_recruiter', methods=['POST'], strict_slashes=False)
def create_new_recruiter():
    """
    Sends form for recruiter creation
    """
    print(request.form)
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
            #Send email to new recruiter with email and password
            return redirect(url_for('recruiter_bp.create_recruiter'))
        return redirect(url_for('recruiter_bp.create_recruiter'))
    except Exception as err:
        print(err)
        return jsonify({'success': False}), 409

@recruiter_bp.route('/recruiter/newBP', methods=['GET'], strict_slashes=False)
def create_BP():
    """
    Sends form for BP creation
    """
    return render_template('recruiter/newBP.html', full_name=fullName, email=email_)

@recruiter_bp.route('/recruiter/profile', methods=['GET'], strict_slashes=False)
def recruiter_profile():
    """
    Displays recruiter's profile
    """
    return render_template('recruiter/Profile.html', full_name=fullName, email=email_)


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
            return redirect(url_for('recruiter_bp.recruiter_login_get'))
        return redirect(url_for('recruiter_bp.recruiter_login_get'))
    except Exception as err:
        print(err)
        return jsonify({'success': False}), 409
    
@recruiter_bp.route('/recruiter/forgot_password', methods=['GET'], strict_slashes=False)
def recruiter_forgot_password():
    """
    TODO: Build this function properly
    resets recruiter password
    """
    return render_template("recruiter/PasswordRecovery.html")


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
                return redirect(url_for('recruiter_bp.recruiter_login_get'))
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

@recruiter_bp.route('/recruiter/create_bp', methods=['POST'], strict_slashes=False)
def bp_creation():
    """
    Creates new business partner OBJ
    """
    print(request.form)
    if not request.form.to_dict():
        abort(400)
    bp_details = request.form.to_dict()
    email = bp_details.get('email')
    full_name = bp_details.get('full_name')
    password = bp_details.get('password')
    
    if not email or not full_name or not password:
        abort(400)
    try:
        business_obj = recruiter.create_business_partner(email, full_name, password)
        
        if business_obj:
            #send email to newly created business partner
            return render_template('recruiter/newBP.html', full_name=fullName, email=email_)
        return jsonify({'success': False}), 500
    except Exception:
        return jsonify({'success': False, 'message': "BP with email {} already exists".format(email)}), 500