""" This is the Applicant controller class """
import backend_core
from sqlalchemy.exc import InvalidRequestError, NoResultFound


class Applicant:
    """ The class for Applicants """

    def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.gender = ""
        self.university = ""
        self.course_of_study = ""
        self.current_employer = ""
        self.current_role = ""
        self.years_of_experience = ""
        self.salary_expectation = 0
        self.other_relevant_information = ""
        #self.image = Column(BLOB)
        #self.resume = Column(BLOB)
        self.applicant_id = ""
        self.email = ""
        self.phone_number = ""

    def create_applicant(self, f_name, l_name, email):
        """ This adds applicants to the DB
        @f_name: first name of the applicant
        @l_name: last name of the applicant
        @email: email of the applicant
        Return: Returns applicant
        """
        try:
            backend_core.db.find_applicant_by(email=email)
        except Exception:
            applicant = backend_core.db.add_applicant(f_name, l_name, email)
            self.applicant_id = applicant.applicant_id
            self.email = applicant.email
            return applicant
        raise ValueError("Applicant with email {} already exists".format(email))

    def update_profile(self, applicant_id, **kwargs):
        """ Updates the user profile
        @kwargs: list of arguments
        Return: Returns a string message
        """
        try:
            applicant = backend_core.db.find_applicant_by(applicant_id=applicant_id)
            backend_core.db.update_applicant(applicant.applicant_id, **kwargs)
            return "Profile updated successfully"
        except Exception as err:
            return err

    def apply(self, applicant_id, job_id):
        """ This function logs every application in the applicants_vacancy table
        """
        try:
            application = backend_core.db.add_applications(applicant_id, job_id)
            print("You have successfuly applied")
        except (InvalidRequestError, NoResultFound) as err:
            print("Application unsuccessful)")
    
    
    # -------------- May 20 Changes Below ------------------ #
    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        if "_sa_instance_state" in dictionary.keys():
            del dictionary["_sa_instance_state"]
        return dictionary