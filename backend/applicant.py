""" This is the Applicant controller class """
from db import DB


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
        self._db = DB()

    def create_applicant(self, f_name, l_name, email):
        """ This adds applicants to the DB
        @f_name: first name of the applicant
        @l_name: last name of the applicant
        @email: email of the applicant
        Return: Returns applicant
        """
        try:
            self._db.find_applicant_by(email=email)
        except Exception:
            return self._db.add_applicant(f_name, l_name, email)
        raise ValueError("Applicant with email {} already exists".format(email))

    def update_profile(self, applicant_id, **kwargs):
        """ Updates the user profile
        @kwargs: list of arguments
        Return: Returns a string message
        """
        try:
            applicant = self._db.find_applicant_by(applicant_id=applicant_id)
            self._db.update_applicant(applicant.applicant_id, **kwargs)
            return "Profile updated successfully"
        except Exception as err:
            return err
