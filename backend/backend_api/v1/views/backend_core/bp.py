""" The business partner module """
import backend_core
from backend_core.model import Base, Vacancy
from flask import g
import uuid
import datetime


class BusinessPartner:
    """ The Business partner Class """
    def create_business_partner(self, email, full_name, password):
        """ Adds a new business partner to the db
        @email: the email of the business partner to be added
        @full_name: the full name of the business partner to be added
        Return: Returns the Business Partner Model object"""
        try:
            backend_core.db.find_business_partner_by(email=email)
        except Exception:
            return backend_core.db.add_business_partner(email, full_name, password)
        raise ValueError("BP with email {} already exists".format(email))

    def update_profile(self, email, **kwargs):
        """ Updates the profile of the Business Partner
        @email: the email of the bp to be updated
        @kwargs: Key value list for updates
        Return: Returns nothing
        """
        try:
            bp = backend_core.db.find_business_partner_by(email=email)
            backend_core.db.update_business_partner(bp.email, **kwargs)
            print("Profile updated successfully")
            return True
        except Exception as err:
            print(err)
            return False


    def make_requisition(self, job_title, department, unit, line_manager,
    number_of_open_positions, location, job_description_summary):
        """ creates a requisition for a vacancy
        @job_title: the job role requisition is made for
        @department: the department the job role sits in
        @unit: the unit the job role sits in
        @line_manager: the line manager the employee to be hired should report to
        @number_of_open_positions: Number of people we are looking to hire
        @location: the location of the job role
        @job_description_summary: The summary of the job
        Return: Returns a vacancy object"""
        try:
            requisition_id = str(uuid.uuid4())
            date_of_requisition = datetime.datetime.now()

            new_vacancy = backend_core.db.add_vacancy(job_title, department, unit, line_manager, number_of_open_positions,
            date_of_requisition, location, job_description_summary, requisition_id)
            return new_vacancy
        except Exception as error:
            print(error)
            return False
    
    def find_business_partner(self, email):
        """
        Uses method in db.py to check existence of business partner
        """
        if not email:
            return False
        try:
            bp = backend_core.db.find_business_partner_by(email=email)
            return bp
        except Exception as error:
            print(error)
            return False
        return True
    
    def delete_business_partner(self, email):
        """
        Deletes business partner from the db
        """
        if not email:
            return False
        try:
            if not self.find_business_partner(email=email):
                return False
            if backend_core.db.delete_business_partner(email=email):
                return True
            return False
        except Exception:
            return False


    
    