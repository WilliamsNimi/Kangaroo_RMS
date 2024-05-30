#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from backend_core.model import Base, Applicant, Recruiter, Vacancy, ApplicantsVacancy, BusinessPartner
import bcrypt
import uuid


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///kangaroo.db")
        # self._engine = create_engine('mysql+mysqldb://root:password@localhost/kangaroo')
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_applicant(self, f_name, l_name, email, password) -> Applicant:
        """ This method adds an applicant to the db
        Return: Returns the new applicant object
        """
        try:
            applicant_id = uuid.uuid4()
            hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            applicant = Applicant(first_name = f_name, last_name = l_name, email = email, applicant_id = str(applicant_id), password = hashed_pwd)
            self._session.add(applicant)
            self._session.commit()
            self._session.refresh(applicant)
            return applicant
        except (InvalidRequestError, NoResultFound) as err:
            self._session.rollback()
            print(err)
            return None

    def add_recruiter(self, email, full_name, password) -> Recruiter:
        """ This method adds a recruiter to the db
        Return: Returns the new recruiter object
        """
        try:
            recruiter_id = uuid.uuid4()
            hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            recruiter = Recruiter(full_name = full_name, email = email, recruiter_id = str(recruiter_id), password = hashed_pwd)
            self._session.add(recruiter)
            self._session.commit()
            self._session.refresh(recruiter)
            return recruiter
        except (InvalidRequestError, NoResultFound) as err:
            self._session.rollback()
            print(err)
            return None

    def add_vacancy(self, j_title, dept, unit, l_manager, no_open_pos,
    date_of_req, location, jd_summary, req_id) -> Vacancy:
        """ This method adds a Vacancy to the db
        Return: Returns the new vacancy object
        """
        try:
            job_id = uuid.uuid4()
            vacancy = Vacancy(job_title = j_title, department = dept, unit = unit, line_manager = l_manager, job_id = str(job_id),
            number_of_open_positions = no_open_pos, date_of_requisition = date_of_req, location = location,
            job_description_summary = jd_summary, requisition_id=req_id, approval_status='Unapproved', publish_status='Unpublished')

            self._session.add(vacancy)
            self._session.commit()
            self._session.refresh(vacancy)
            return vacancy
        except (InvalidRequestError, NoResultFound) as err:
            self._session.rollback()
            print(err)
            return None

    def find_applicant_by(self, **kwargs) -> Applicant:
        """ A method to search the db
        @query_str: the query to search for
        Return: Returns the first row wher the applicant is found
        """
        applicants = self._session.query(Applicant)
        if not applicants:
            raise NoResultFound
        if not kwargs:
            raise InvalidRequestError
        for key in kwargs.keys():
            if not hasattr(Applicant, key):
                raise InvalidRequestError
            if key == 'password':
                del kwargs[key]
        applicant_found = self._session.query(Applicant).filter_by(**kwargs).first()
        if not applicant_found:
            raise NoResultFound
        return applicant_found

    def find_recruiter_by(self, **kwargs) -> Recruiter:
        """ A method to search the db
        @query_str: the query to search for
        Return: Returns the first row where the recruiter is found
        """
        recruiters = self._session.query(Recruiter)
        if not recruiters:
            raise NoResultFound
        if not kwargs:
            raise InvalidRequestError
        for key in kwargs.keys():
            if not hasattr(Recruiter, key):
                raise InvalidRequestError
            if key == 'password':
                del kwargs[key]
        recruiter_found = self._session.query(Recruiter).filter_by(**kwargs).first()
        if not recruiter_found:
            raise NoResultFound
        return recruiter_found
    
    def find_vacancy_by(self, **kwargs) -> Vacancy:
        """ A method to search the db
        @query_str: the query to search for
        Return: Returns the first row where the vacancy is found
        """
        vacancies = self._session.query(Vacancy)
        if not vacancies:
            raise NoResultFound
        if not kwargs:
            raise InvalidRequestError
        for key in kwargs.keys():
            if not hasattr(Vacancy, key):
                raise InvalidRequestError
        vacancy_found = self._session.query(Vacancy).filter_by(**kwargs).first()
        if not vacancy_found:
            raise NoResultFound
        return vacancy_found

    def update_applicant(self, applicant_id, **kwargs) -> None:
        """ This method updates applicants table based on id
        @applicant_id: user Id to be found
        Return: Returns none
        """
        try:
            applicant = self.find_applicant_by(applicant_id=applicant_id)
            for key, value in kwargs.items():
                if not hasattr(Applicant, key):
                    raise ValueError
                else:
                    if key == 'password':
                        value = bcrypt.hashpw(str(value).encode('utf-8'), bcrypt.gensalt())
                    setattr(applicant, key, value)
            self._session.commit()
            return True
        except Exception:
            self._session.rollback()
            return None

    def update_recruiter(self, recruiter_id, **kwargs) -> None:
        """ This method updates recruiters table based on id
        @recruiter_id: recruiter Id to be found
        Return: Returns none
        """
        try:
            recruiter = self.find_recruiter_by(recruiter_id=recruiter_id)
            for key, value in kwargs.items():
                if not hasattr(Recruiter, key):
                    raise ValueError
                else:
                    if key == 'password':
                        value = bcrypt.hashpw(str(value).encode('utf-8'), bcrypt.gensalt())
                    setattr(recruiter, key, value)
            self._session.commit()
            return True
        except Exception:
            return None

    def update_vacancy(self, job_id, **kwargs) -> None:
        """ This method updates vacancy table based on id
        @job_id: job Id to be found
        Return: Returns none
        """
        try:
            vacancy = self.find_vacancy_by(job_id=job_id)
            for key, value in kwargs.items():
                if not hasattr(Vacancy, key):
                    raise ValueError
                else:
                    setattr(vacancy, key, value)
            self._session.commit()
            return True
        except Exception:
            return None

    def add_applications(self, applicant_id, job_id):
        """ This function logs every application in the applicants_vacancy table
        """
        try:
            application = ApplicantsVacancy(applicant_id = applicant_id, job_id = job_id)
            self._session.add(application)
            self._session.commit()
            self._session.refresh(application)
            print("You have a new application")
            return application
        except (InvalidRequestError, NoResultFound) as err:
            self._session.rollback()
            print(err)
            return None
    
    def add_business_partner(self, email, full_name, password):
        """ Add a new business partner
        @email: email of the business partner
        @full_name: full name of the business partner
        Return: the BusinessPartner object """
        try:
            hashed_pwd = bcrypt.hashpw(str(password).encode('utf-8'), bcrypt.gensalt())
            business_partner = BusinessPartner(email = email, full_name = full_name, password = hashed_pwd)
            self._session.add(business_partner)
            self._session.commit()
            self._session.refresh(business_partner)
            return business_partner
        except (InvalidRequestError, NoResultFound) as err:
            self._session.rollback()
            print(err)
            return None

    def find_business_partner_by(self, **kwargs) -> BusinessPartner:
        """ A method to search the db
        @query_str: the query to search for
        Return: Returns the first row wher the applicant is found
        """
        bps = self._session.query(BusinessPartner)
        if not bps:
            raise NoResultFound
        if not kwargs:
            raise InvalidRequestError
        for key in kwargs.keys():
            if not hasattr(BusinessPartner, key):
                raise InvalidRequestError
        bp_found = self._session.query(BusinessPartner).filter_by(**kwargs).first()
        if not bp_found:
            raise NoResultFound
        return bp_found

    def update_business_partner(self, email, **kwargs) -> None:
        """ This method updates business partner table based on email
        @email: email to be found
        Return: Returns none
        """
        try:
            bp = self.find_business_partner_by(email=email)
            for key, value in kwargs.items():
                if not hasattr(BusinessPartner, key):
                    raise ValueError
                else:
                    if key == 'password':
                        value = bcrypt.hashpw(str(value).encode('utf-8'), bcrypt.gensalt())
                    setattr(bp, key, value)
            self._session.commit()
        except Exception:
            return None

    def find_applicants_by(self, **kwargs) -> Applicant:
        """ A method to search the db
        @kwargs: Key Value items to search for in the db
        Return: Returns all records in the table with matching substring
        """
        applicants = self._session.query(Applicant)
        if not applicants:
            raise NoResultFound
        if not kwargs:
            raise InvalidRequestError

        filters = []

        for key, value in kwargs.items():
            if not hasattr(Applicant, key):
                raise InvalidRequestError
            filters.append(getattr(Applicant, key).like(f"%{value}%"))

        applicants_found = applicants.filter(*filters).all()
        if not applicants_found:
            raise NoResultFound
        return applicants_found


    def delete_vacancy(self, job_id):
        """Deletes a vacancy from db
        
        Keyword arguments:
        @job_id: Job object with the provided ID
        Return: Boolean
        """
        if not job_id:
            return False
        try:
            vacancy_object = self.find_vacancy_by(job_id=job_id)
            self._session.delete(vacancy_object)
            self._session.commit()
            return True
        except Exception:
            return False

    def show_all_vacancies(self):
        """Displays all the vacancies in the vacancy table"""
        vacancy_list = []
        vacancies = self._session.query(Vacancy).all()
        for vacancy in vacancies:
            vacancy_list.append(vacancy.job_id)
        return vacancy_list

    def show_all_recruiters(self):
        """Displays all the vacancies in the vacancy table"""
        recruiter_list = []
        recruiters = self._session.query(Recruiter).all()
        for recruiter in recruiters:
            recruiter_list.append(recruiter.recruiter_id)
        return recruiter_list

    def show_all_bps(self):
        """Displays all the vacancies in the vacancy table"""
        bp_list = []
        bps = self._session.query(BusinessPartner).all()
        for bp in bps:
            bp_list.append(bp.email)
        return bp_list

    def show_all_applicants(self):
        """Displays all the vacancies in the vacancy table"""
        applicant_list = []
        applicants = self._session.query(Applicant).all()
        for applicant in applicants:
            applicant_list.append((applicant.first_name, applicant.email))
        return applicant_list

    def delete_recruiter(self, recruiter_id):
        """ This method Deletes a recruiter from the db
            Returns Boolean
        """
        if not recruiter_id:
            return False
        try:
            recruiterObj = self.find_recruiter_by(recruiter_id=recruiter_id)
            self._session.delete(recruiterObj)
            self._session.commit()
            return True
        except (InvalidRequestError, NoResultFound) as err:
            self._session.rollback()
            print(err)
            return False

    def delete_business_partner(self, email):
        """ This method Deletes a recruiter from the db
            Returns Boolean
        """
        if not email:
            return False
        try:
            bpObj = self.find_business_partner_by(email=email)
            self._session.delete(bpObj)
            self._session.commit()
            return True
        except (InvalidRequestError, NoResultFound) as err:
            self._session.rollback()
            print(err)
            return False
    
    def find_recruiter_vacancies_by(self, recruiter_id):
        """ A method to retrieve all vacancies of recruiter - the approved
            and unapproved
        recruiter_id: the query to search for
        Return: List of vacancies of the recruiter
        """
        if not recruiter_id:
            raise InvalidRequestError
        vacancies = self._session.query(Vacancy)
        if not vacancies:
            raise NoResultFound
        if not hasattr(Vacancy, 'recruiter_id'):
            raise InvalidRequestError
        vacancies_found = self._session.query(Vacancy).filter_by(recruiter_id=recruiter_id).all()
        if not vacancies_found:
            raise NoResultFound
        vacancy_list = []

        for vacancy in vacancies_found:
            vacancy_list.append(self.to_dict(vacancy))
        return vacancy_list
    
    def close(self):
        """
        Closes current session with the db for each API request
        """
        self._session.close()

 

# dictionary['date_of_requisition'] = object.date_of_requisition.isoformat()
