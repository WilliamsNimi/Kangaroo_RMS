#!/usr/bin/env python3
"""
Authentication for recruiter implementation
"""
import backend_core
import bcrypt


class RecruiterAuth:
    """
    Authentication for recruiter class implementation
    """
    def verify_credentials(self, **kwargs):
        """
        Verifies credentials of recruiter
        """
        from backend_core.model import Recruiter

        if not kwargs or len(kwargs.keys()) < 2:
            return False
        try:
            password = None
            kkeys = kwargs.copy()
            for key in kkeys.keys():
                if not hasattr(Recruiter, key):
                    return False
                if key == 'password':
                    password = kwargs[key]
                    del kwargs[key]
            recruiter = backend_core.db.find_recruiter_by(**kwargs)
            if recruiter and password:
                if bcrypt.checkpw(password.encode('utf-8'), recruiter.password.encode('utf-8')):
                    return ['recruiter_id', recruiter.recruiter_id]
            return False
        except Exception as error:
            print(error)
            return False


class ApplicantAuth:
    """
    Authentication for Applicant object
    """
    def verify_credentials(self, **kwargs):
        """
        Verifies credentials of applicant
        """
        from backend_core.model import Applicant

        if not kwargs or len(kwargs.keys()) < 2:
            return False
        try:
            password = None
            kkeys = kwargs.copy()
            for key in kkeys.keys():
                if not hasattr(Applicant, key):
                    return False
                if key == 'password':
                    password = kwargs[key]
                    del kwargs[key]
            applicant = backend_core.db.find_applicant_by(**kwargs)
            if applicant and password:
                if bcrypt.checkpw(password.encode('utf-8'), applicant.password.encode('utf-8')):
                    return ['applicant_id', applicant.applicant_id]
            return False
        except Exception as error:
            print(error)
            return False


class BPAuth:
    """
    Authentication for recruiter class
    """
    def verify_credentials(self, **kwargs):
        """
        Verifies credentials of recruiter
        """
        from backend_core.model import BusinessPartner

        if not kwargs or len(kwargs.keys()) < 2:
            return False
        try:
            password = None
            kkeys = kwargs.copy()
            for key in kkeys.keys():
                if not hasattr(BusinessPartner, key):
                    return False
                if key == 'password':
                    password = kwargs[key]
                    del kwargs[key]
            bp = backend_core.db.find_business_partner_by(**kwargs)
            if bp and password:
                if bcrypt.checkpw(password.encode('utf-8'), bp.password.encode('utf-8')):
                    return ['email', bp.email]
            return False
        except Exception as error:
            print(error)
            return False

# bp = BPAuth()
# rec = RecruiterAuth()
# app = ApplicantAuth()
