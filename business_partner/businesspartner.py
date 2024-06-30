""" 
TODO:
        1. Give Business Partner list of available recruiters to choose from.
        2. Only roles a business partner raised should be visible to them.

        GLOBAL: 
        1. Implement password Regex.
        2. Implement SQL injection checks for all forms.
        3. Implement Session Management for Logout.
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
    """
    jobs = bp.show_all_vacancies()
    return render_template("businesspartner/Home.html", email=email_, full_name=fullName, jobs=jobs)

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
    """

    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        bp_= bp.find_business_partner(email)
        global email_
        global fullName
        try:
            email_ = bp_.email
            fullName = bp_.full_name
            p_bytes = password.encode('utf-8')
            hashed_password_val = bcrypt.checkpw(p_bytes, bp_.password)
            if hashed_password_val and email == bp_.email:
                return redirect(url_for("business_partner_bp.bp_homepage", email=email_, full_name=fullName))
        except Exception:
            error_message =  "Username or Password incorrect"
    return render_template("businesspartner/SignIn.html", error_message=error_message)


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
    Makes a requisition
    """

    if request.method == 'POST':
        job_title = request.form['job_title']
        department = request.form['department']
        unit = request.form['unit']
        line_manager = request.form['line_manager']
        number_of_open_positions = request.form['no_open_positions']
        location = request.form['location']
        job_description_summary = request.form['jd_summary']
        bp.make_requisition(job_title, department, unit, line_manager, number_of_open_positions, location, job_description_summary)
        return redirect(url_for("business_partner_bp.bp_homepage"))
    return redirect(url_for("business_partner_bp.bp_homepage"))

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