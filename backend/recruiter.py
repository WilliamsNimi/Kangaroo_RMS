""" This is the Recruiter controller class """
from db import DB


class Recruiter:
    """ The Controller class """
    def __init__(self):
        """ Constructor initialization """
        self.email = ""
        self.full_name = ""
        self.job_role = "Recruiter"
        self.number_of_roles_assigned = 0
        self._db = DB()

    def create_recruiter(self, email, full_name):
        """ adds a new recruiter 
        @email: email address of the recruiter
        @full_name: full name of the recruiter"""
        try:
            self._db.find_recruiter_by(email=email)
        except Exception:
            return self._db.add_recruiter(email, full_name)
        raise ValueError("Recruiter with email {} already exists".format(email))

    def update_profile(self, recruiter_id, **kwargs):
        """ Updating the recruiter profile
        @recruiter_id: the id of the recruiter profile to be found
        @kwargs: key value arguments to be updated
        Return: Returns nothing"""
        try:
            recruiter = self._db.find_recruiter_by(recruiter_id=recruiter_id)
            self._db.update_recruiter(recruiter_id, **kwargs)
            return "Profile updated successfully"
        except Exception as err:
            return err