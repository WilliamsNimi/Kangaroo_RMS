""" 
1. make_requisition /requisitions POST 'makes a vacancy request to the recruiter'
"""
from flask import request, abort, render_template, jsonify, url_for
from flask import g, redirect, make_response
from backend_core import bp
from backend_auth import bp_auth, session_auth
from flask import Blueprint
import bcrypt

email_ = ""
fullName = ""

# Defining a blueprint
business_partner_bp = Blueprint(
    'business_partner_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@business_partner_bp.route('/bp/home', methods=['GET'], strict_slashes=False)
def bp_home():
    """
    Signin page of business partner
    """
    return render_template("businesspartner/SignIn.html")

@business_partner_bp.route('/bp/forgot_password', methods=['GET'], strict_slashes=False)
def bp_forgot_password():
    """
    Home page of business partner
    """
    return render_template("businesspartner/PasswordRecovery.html")

@business_partner_bp.route('/bp/profile', methods=['GET'], strict_slashes=False)
def bp_profile():
    """
    profile page of business partner
    """
    return render_template("businesspartner/Profile.html")

@business_partner_bp.route('/bp/homepage', methods=['GET'], strict_slashes=False)
def bp_homepage():
    """
    Home page of business partner
    jsonify({'success': True, 'message': 'Welcome Home Business Partner!'})
    """
    return render_template("businesspartner/Home.html", email=email_, full_name=fullName)

@business_partner_bp.route('/bp/login', methods=['GET'], strict_slashes=False)
def bp_login_get():
    """
    Business Partner login
    
    session_token = request.cookies.get('session_token')
    
    if session_token:
        bp_details = session_auth.verify_session(session_token)
        if bp_details:
            setattr(g, bp_details[0], bp_details[1])
            return redirect(url_for('business_partner_bp.bp_home'))"""
    return render_template("businesspartner/SignIn.html")



@business_partner_bp.route('/bp/login', methods=['POST'], strict_slashes=False)
def bp_login_post():
    """
    Business Partner login
    try:
        bp_dict = request.form.to_dict()
        if bp_dict:
            bp_details = bp_auth.verify_credentials(**bp_dict)
            if bp_details:
                setattr(g, bp_details[0], bp_details[1])
                response = make_response(redirect(url_for('business_partner_bp.bp_homepage')))
                session_token = session_auth.create_session('business_partner', bp_details[1])
                response.set_cookie(
                    'session_token', 
                    str(session_token), 
                    httponly=True, 
                    secure=False, 
                    path='/kangaroo/v1/bp'
                    # samesite='Lax'
                )
                return response
        return redirect(url_for('business_partner_bp.bp_login_get'))
    except Exception as error:
        print(error)
        return redirect(url_for('business_partner_bp.bp_login_get'))"""

    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        bp_= bp.find_business_partner(email)
        global email_
        global fullName
        email_ = bp_.email
        fullName = bp_.full_name
        p_bytes = password.encode('utf-8')
        hashed_password_val = bcrypt.checkpw(p_bytes, bp_.password)
        if hashed_password_val and email == bp_.email:
            return render_template("businesspartner/Home.html", email=email_, full_name=fullName)
    return render_template("businesspartner/SignIn.html")


@business_partner_bp.route('/bp/logout', methods=['POST'], strict_slashes=False)
def bp_logout():
    """
    Logs out currently logged in user
    """
    from backend_api.v1.app import app

    session_token = request.cookies.get('session_token')
    if session_token:
        session_auth.delete_session(session_token)
        return redirect(url_for('home'))
    return jsonify({'error': 'session token not found'}), 404


@business_partner_bp.route('/bp/requisitions', methods=['GET'], strict_slashes=False)
def bp_create_requisition():
    """
    Returns template to create vacancy requisition
    """
    return render_template('businesspartner/Requisition.html', email=email_, full_name=fullName)


@business_partner_bp.route('/bp/signup', methods=['GET'], strict_slashes=False)
def create_bp():
    """
    Sends form for business creation
    """
    return render_template('new_bp.html')


@business_partner_bp.route('/bp/requisitions', methods=['POST'], strict_slashes=False)
def bp_post_vacancy():
    """
    Creates job to be posted if requisition-id exists
    
    if not request.form.to_dict():
        abort(400)
    vacancy_details = request.form.to_dict()
    vacancy_list = ['job_title', 'department', 'unit',
                'line_manager', 'number_of_open_positions',
                'location', 'job_description_summary', 'recruiter_id']
    if not all(vacancy_details.get(detail) for detail in vacancy_list):
        abort(400)
    job_title = vacancy_details.get('job_title')
    department = vacancy_details.get('department')
    unit = vacancy_details.get('unit')
    line_manager = vacancy_details.get('line_manager')
    number_of_open_positions = vacancy_details.get('no_open_positions')
    location = vacancy_details.get('location')
    job_description_summary = vacancy_details.get('jd_summary')
    
    try:
        vacancy_created = bp.make_requisition(job_title, department, unit, line_manager, number_of_open_positions, 
                                              location, job_description_summary) 
        if vacancy_created:
            del vacancy_created.__dict__["_sa_instance_state"]
            vacancy_created.__dict__['__class__'] = (str(type(vacancy_created)).split('.')[-1]).split('\'')[0]
            vacancy_created.__dict__['date_of_requisition'] = vacancy_created.date_of_requisition.isoformat()
            return jsonify({'success': True, 'vacancy': vacancy_created.__dict__}), 201
    except Exception as error:
        print(error)
        return jsonify({'success': False}), 500 """

    if request.method == 'POST':
        job_title = request.form['job_title']
        department = request.form['department']
        unit = request.form['unit']
        line_manager = request.form['line_manager']
        number_of_open_positions = request.form['no_open_positions']
        location = request.form['location']
        job_description_summary = request.form['jd_summary']
        vacancy_created = bp.make_requisition(job_title, department, unit, line_manager, number_of_open_positions, location, job_description_summary)
        return render_template("businesspartner/Home.html", job_title=vacancy_created.job_title, location=vacancy_created.location, number=vacancy_created.number_of_open_positions, status=vacancy_created.approval_status)
    return render_template("businesspartner/SignIn.html")

@business_partner_bp.route('/bp/profile/update', methods=['PUT'], strict_slashes=False)
def bp_update_profile():
    """
    Updates profile of the business partner
    """
    if not request.form.to_dict():
        abort(400)
    update_details = request.form.to_dict()
    update_details.pop('email', None)
    update_details.pop('id', None)
    email = g.email

    if not email:
        abort(404)
    try:
        if bp.update_profile(email, **update_details):
            if 'password' in update_details:
                session_token = request.cookies.get('session_token')
                session_auth.delete_session(session_token)
                return redirect(url_for('kangaroo.bp_login_get'))
            return jsonify({'success': True})
        return jsonify({'success': False}), 500
    except Exception as error:
        print(error)
        return jsonify({'success': False}), 500

@business_partner_bp.route('/bp/profile/delete', methods=['DELETE'], strict_slashes=False)
def bp_delete():
    """
    Deletes BP object from the database
    """
    email = g.email
    if not email:
        abort(404)
    try:
        if not bp.find_business_partner(email):
            abort(404)
        success = bp.delete_business_partner(email=email)
        if success:
            session_token = request.cookies.get('session_token')
            session_auth.delete_session(session_token)
            return jsonify({'success': True})
        return jsonify({'success': False}), 500 
    except Exception as error:
        print(error)
        return jsonify({'success': False}), 500