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
        
    
    # --------------------- I(JBA) ADDED THE METHODS BELOW --------------------------- #
    
    # def find_vacancy(self, job_id):
    #     """Attempts finding vacancy from the db
        
    #     Keyword arguments:
    #     @job_id: Identifies a specific vacancy object
    #     Return: Boolean
    #     """
    #     try:
    #        self._db.find_vacancy_by(job_id=job_id)
    #        return True
    #     except Exception:
    #         return False
    
    def delete_job(self, job_id):
        """
        Deletes job from the db if it exists
        @job_id: ID of job to be deleted
        Returns: Boolean
        """
        return self._db.delete_vacancy(job_id=job_id)
    
    def boolean_search(self, **kwargs):
        """Searches for applicants with mathing attributes
        Return: applicant objects matching the provided attributes
        """
        if not kwargs:
            return False
        try:
            applicants_found = self._db.find_applicants_by(**kwargs)
            applicants_list = []
            if applicants_found:
                for applicant in applicants_found:
                    applicants_list.append(applicant.__dict__)
                return applicants_list
            return None
        except Exception:
            return None
        
        
        