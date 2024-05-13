""" The business partner module """
from db import DB
from model import Base, Vacancy
import uuid
import datetime


class BusinessPartner:
    """ The Business partner Class """
    def __init__(self):
        self._db = DB()

    def create_business_partner(self, email, full_name):
        """ Adds a new business partner to the db
        @email: the email of the business partner to be added
        @full_name: the full name of the business partner to be added
        Return: Returns the Business Partner Model object"""
        try:
            self._db.find_business_partner_by(email=email)
        except Exception:
            self.full_name = full_name
            return self._db.add_business_partner(email, full_name)
        raise ValueError("BP with email {} already exists".format(email))

    def update_profile(self, email, **kwargs):
        """ Updates the profile of the Business Partner
        @email: the email of the bp to be updated
        @kwargs: Key value list for updates
        Return: Returns nothing
        """
        try:
            bp = self._db.find_business_partner_by(email=email)
            self._db.update_business_partner(bp.email, **kwargs)
            return "Profile updated successfully"
        except Exception as err:
            return err


    def make_requisition(self, job_title, department, unit, line_manager,
    number_of_open_positions, location, job_description_summary):
        """ creates a requisition for a vacancy
        @job_title: the job role requisition is made for
        @department: the department the job role sits in
        @unit: the unit the job role sits in
        @line_manager: the line manager the employee to be hired should report to
        @number_of_open_positions: Number of people we are looking to hire
        @location: the location of the job role
        @recruiter_id: The recruiter requested for
        @job_description_summary: The summary of the job
        Return: Returns a vacancy object"""

        requisition_id = str(uuid.uuid4())
        date_of_requisition = datetime.datetime.now()
        bp_name = self.full_name

        new_vacancy = self._db.add_vacancy(job_title, department, unit, line_manager, number_of_open_positions,
        date_of_requisition, bp_name, location, job_description_summary, requisition_id)
        return new_vacancy
    

    #   ------------------------------ I(JBA) ADDED THE FUNCTIONS BELOW -----------------------------   #



    
    