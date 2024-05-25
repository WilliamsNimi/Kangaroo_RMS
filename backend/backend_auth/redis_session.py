#!/usr/bin/env python3
"""
Redis Session authentication implementation
"""
import backend_core
import redis
from uuid import uuid4
from flask import g


class RedisSession:
    """
    Session management with redis
    """
    def __init__(self):
        """
        Redis instance initialisation
        """
        self._redis = redis.Redis(host='127.0.0.1', port=6379, db=0)
    
    @property
    def session(self):
        """
        Access redis connection to db
        """
        return self._redis
    
    def verify_session(self, session_token):
        """
        Verifies existence of session ID in db
        and verifies existence of userID
        """
        if not session_token:
            return False
        user_id = self._redis.get(str(session_token))
        
        if user_id:
            user_type = user_id.decode('utf8').split('_')[0]
            try:
                if user_type == 'applicant':
                    applicant_id = user_id.decode('utf8').split('_')[1]
                    backend_core.db.find_applicant_by(applicant_id=applicant_id)
                    return ['applicant_id', applicant_id]
                if user_type == 'recruiter':
                    recruiter_id = user_id.decode('utf8').split('_')[1]
                    backend_core.db.find_recruiter_by(recruiter_id=recruiter_id)
                    return ['recruiter_id', recruiter_id]
                if user_type == 'business_partner':
                    email = user_id.decode('utf8').split('_')[1]
                    backend_core.db.find_business_partner_by(email=email)
                    return ['email', email]
            except Exception:
                return False
        return False
    
    def create_session(self, user_type, key_attribute=None):
        """
        Creates user session with user Type and attribute to set
        """
        if not user_type or not key_attribute:
            return False
        if user_type in ['business_partner', 'recruiter', 'applicant']:
            session_token = uuid4()
            self._redis.set(str(session_token), "{}_{}".format(user_type, key_attribute), ex=5000)
            return session_token
        return False
    
    def delete_session(self, session_token):
        """
        Deletes a user session token
        """
        if not session_token:
            return False
        self._redis.delete(session_token)
        return True

    def session_authorization(self, session_token):
        """
        session authorization logic implementation
        """
        if session_token:
            user_detail = self.verify_session(session_token)
            
            if user_detail:
                setattr(g, user_detail[0], user_detail[1])
                return True
        return False

    def needs_authentication(self, path):
        """
        Checks if path needs authentication
        """
        excluded_paths = ['/kangaroo/v1/applicant/new/', '/kangaroo/v1/recruiter/new/', '/kangaroo/v1/bp/new/', '/kangaroo/v1/recruiter/login/'
                          '/kangaroo/v1/recruiter/logout/', '/kangaroo/v1/bp/login/', '/kangaroo/v1/bp/logout/', '/kangaroo/v1/applicant/login/',
                          '/kangaroo/v1/applicant/logout/']

        if not path:
            return True
        if path[-1] != '/':
            if path + '/' in excluded_paths:
                return False
        for p in excluded_paths:
            if p.endswith('*'):
                if path.startswith(p[:-1]):
                    return False
            if p == path:
                return False
        return True







""" Applicant
[1] /applicant/login
URL::
curl -i -X POST -H 'Content-type: application/json' -d '{"email": "nimiwilliams@gmail.com", "password": "password"}'  http://127.0.0.1:5000/kangaroo/v1/applicant/login

[2] /applicant/logout
URL::
curl -i -b 'session_token=2037cc85-4392-4c8d-8e48-a3b130029308' -X POST http://127.0.0.1:5000/kangaroo/v1/applicant/logout

[3] /applicant/home
URL::
curl -i  -X GET http://127.0.0.1:5000/kangaroo/v1/applicant/home


ALL OTHER ENDPOINTS ARE OF STRUCTURE
"""
