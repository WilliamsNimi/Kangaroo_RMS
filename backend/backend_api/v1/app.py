#!/usr/bin/env python3
"""
Kangaroo API application implementation
"""
from backend_api.v1.views import kangaroo
from flask import Flask, request, g, jsonify, abort
import backend_auth


app = Flask(__name__)
app.register_blueprint(kangaroo)


@app.before_request
def before_request():
    """
    Checks for authorization
    """
    if backend_auth.session_auth.needs_authentication(request.path):
        session_token = request.cookies.get('session_token')
        if session_token:
            if not backend_auth.session_auth.session_authorization(session_token):
                abort(403)
        else:
            abort(401)
    

@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    """
    Home route
    """
    return jsonify({'success': True, 'message': 'Welcome to General Home!'})

@app.teardown_appcontext
def close_db_session(error):
    """
    Automatically closes connection to the db
    """
    from backend_core import db
    db.close()

@app.errorhandler(404)
def not_found(error):
    """
    Handles NOT FOUND error
    """
    return jsonify({'error': 'Not Found'}), 404

@app.errorhandler(400)
def bad_request(error):
    """
    Handles BAD REQUEST error
    """
    return jsonify({'error': 'Bad Request'}), 400

@app.errorhandler(401)
def unauthorized_request(error):
    """
    Handles UNAUTHORIZED REQUEST error
    """
    return jsonify({'error': 'Unauthorized'}), 401

@app.errorhandler(500)
def server_error(error):
    """
    Handles SERVER ERROR error
    """
    return jsonify({'error': 'Server Error'}), 500

@app.errorhandler(409)
def conflict(error):
    """
    Handles CONFLICT ERROR error
    """
    return jsonify({'error': 'Conflict'}), 409


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)







""" ------ APPLICANT VIEW TESTS ------
[1] /applicant/new
URL::
curl -i -X POST -H 'Content-type: application/json' -d '{"first_name": "Nimi", "last_name": "Williams", "email": "nimiwilliams@gmail.com", "password": "password"}
'  http://127.0.0.1:5000/kangaroo/v1/applicant/new

RESPONSE::
{"applicant":{"__class__":"Applicant","applicant_id":"fcb12c25-803b-4a65-a24e-abdca014afb4","course_of_study":null,"current_employer":null,"current_role":null,"email":"nimiwilliams@gmail.com","first_name":"Nimi","gender":null,"id":null,"image":null,"last_name":"Williams","other_relevant_information":null,"phone_number":null,"resume":null,"salary_expectation":null,"university":null,"years_of_experience":null},"success":true}


[2] /applicant/apply
URL:: 
curl -X POST -H 'Content-type: application/json' -d '{"applicant_id": "3ddacc3d-5194-4399-9ed4-3d24663e454a", "job_id": "77764e98-e651-4e8b-8648-0f1afb9a98c4"}' http://127.0.0.1:5000/kangaroo/v1/applicant/apply

RESPONSE::
{"success":true}


[3] /applicant/profile/update
URL::
curl -X POST -H 'Content-type: application/json' -d '{"applicant_id": "fcb12c25-803b-4a65-a24e-abdca014afb4", "course_of_study":"Computer Science","current_employer":"Nimi Williams","current_role":"Frontend engineer"}' http://127.0.0.1:5000/kangaroo/v1/applicant/profile/update

RESPONSE::
{"success":true}


[4]

"""





""" BUSINESS PARTNER VIEW TESTS

[1] /bp/requisitions
URL::
curl -X POST -H 'Content-type: application/json' -d '{"job_title": "Backend-engineer", "department": "IT", "unit": "Some Unit", "line_manager": "Fiifi", "number_of_open_positions": 5, "location": "Accra", "job_description_summary": "Prepare for battle", "recruiter_id": "6cf951c5-fdbd-4d79-b863-52a3bafda045"}' http://127.0.0.1:5000/kangaroo/v1/bp/requisitions

RESPONSE::
{"success":true,"vacancy":{"__class__":"Vacancy","approval_status":null,"business_partner":"Temporary Business Partner","date_of_requisition":"Wed, 22 May 2024 00:42:05 GMT","department":"IT","id":null,"job_description":null,"job_description_summary":"Prepare for battle","job_id":"6fbc9bb8-c6bc-4f0c-84b0-1f8daa3754f4","job_title":"Backend-engineer","line_manager":"Fiifi","location":"Accra","number_of_open_positions":5,"publish_status":null,"recruiter_id":null,"requisition_id":"23904f58-c5a8-4e42-bacb-bbdec806f64e","unit":"Some Unit"}}


[2] /bp/new
URL::
curl -X POST -H 'Content-type: application/json' -d '{"email": "joshua123@gmail.com", "full_name": "JBA"}' http://localhost:5000/kangaroo/v1/bp/new

RESPONSE::
{"success":true,"vacancy":{"__class__":"BusinessPartner","email":"joshua123@gmail.com","full_name":"JBA","id":1}}


[3] /bp/profile/update
URL::
curl -X PUT -H 'Content-type: application/json' -d '{"email": "joshua123@gmail.com", "full_name": "A_VERY_LONG_NAME"}' http://localhost:5000/kangaroo/v1/bp/profile/update

RESPONSE::
{"success":true}

"""




""" RECRUITER VIEW TESTS
[1] /recruiter/new

URL::
curl -X POST -H 'Content-type: application/json' -d '{"email": "iam_a_recruiter@work.com", "full_name": "I have an awesome name"}' http://127.0.0.1:5000/kangaroo/v1/recruiter/new

RESPONSE::
{"recruiter":{"__class__":"Recruiter","email":"iam_a_recruiter@work.com","full_name":"I have an awesome name","id":null,"job_role":null,"number_of_roles_assigned":null,"recruiter_id":"56db1531-e8b9-41b1-8015-b5a9406b897c"},"success":true}


[2] /recruiter/delete/<recruiter_id>
URL::
curl -X DELETE  http://127.0.0.1:5000/kangaroo/v1/recruiter/delete/56db1531-e8b9-41b1-8015-b5a9406b897c

RESPONSE::
NO RESPONSE (AS EXPECTED)


[3] /recruiter/jobs/<job_id>
URL::
curl -i -X DELETE  http://127.0.0.1:5000/kangaroo/v1/recruiter/jobs/6fbc9bb8-c6bc-4f0c-84b0-1f8daa3754f4

RESPONSE::
NO RESPONSE (AS EXPECTED)


[4] /recruiter/vacancies/<recruiter_id>
URL:: 
curl -i -X GET  http://127.0.0.1:5000/kangaroo/v1/recruiter/vacancies/a49abf74-4946-4078-b485-db083cc89c0b

RESPONSE::
EXPECTED RESPONSE :)


"""