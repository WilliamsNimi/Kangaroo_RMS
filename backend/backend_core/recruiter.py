""" This is the Recruiter controller class """
import backend_core

class Recruiter:
    """ The Controller class """
    def __init__(self):
        """ Constructor initialization """
        self.email = ""
        self.full_name = ""
        self.job_role = "Recruiter"
        self.number_of_roles_assigned = 0

    def create_recruiter(self, email, full_name):
        """ adds a new recruiter 
        @email: email address of the recruiter
        @full_name: full name of the recruiter"""
        try:
            backend_core.db.find_recruiter_by(email=email)
        except Exception:
            return backend_core.db.add_recruiter(email, full_name)
        raise ValueError("Recruiter with email {} already exists".format(email))

    def update_profile(self, recruiter_id, **kwargs):
        """ Updating the recruiter profile
        @recruiter_id: the id of the recruiter profile to be found
        @kwargs: key value arguments to be updated
        Return: Returns nothing"""
        try:
            recruiter = backend_core.db.find_recruiter_by(recruiter_id=recruiter_id)
            backend_core.db.update_recruiter(recruiter_id, **kwargs)
            return "Profile updated successfully"
        except Exception as err:
            return err

    def update_vacancy(self, job_id, **kwargs):
        """ Updates the Vacancy with the given job_id
        @job_id: Vacancy to search for
        @Return: Returns update status
        """
        try:
            vacancy = backend_core.db.find_vacancy_by(job_id=job_id)
            backend_core.db.update_vacancy(vacancy.job_id, **kwargs)
            return "Vacancy updated successfully"
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
    #        dbObject.find_vacancy_by(job_id=job_id)
    #        return True
    #     except Exception:
    #         return False
    
    def delete_job(self, job_id):
        """
        Deletes job from the db if it exists
        @job_id: ID of job to be deleted
        Returns: Boolean
        """
        return backend_core.db.delete_vacancy(job_id=job_id)
    
    # ------------ MAY 20 Changes Below ------------ #
    
    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        if "_sa_instance_state" in dictionary.keys():
            del dictionary["_sa_instance_state"]
        return dictionary
    
    def find_recruiter(self, recruiter_id):
        """
        Find a recruiter obj based on recruiter_id
        """
        if not recruiter_id:
            return False
        try:
            backend_core.db.find_recruiter_by(recruiter_id=recruiter_id)
            return True
        except Exception:
            return False
    
    def delete_recruiter(self, recruiter_id):
        """
        Deletes a recruiter obj from the db
        """
        if not recruiter_id:
            return False
        try:
            backend_core.db.find_recruiter_by(recruiter_id=recruiter_id)
            backend_core.db.delete_recruiter(recruiter_id)
            return True
        except Exception:
            return False
        
        
        