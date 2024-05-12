#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from model import Base, Applicant, Recruiter, Vacancy, ApplicantsVacancy
import uuid


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///kangaroo.db")
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

    def add_applicant(self, f_name, l_name, email) -> Applicant:
        """ This method adds an applicant to the db
        Return: Returns the new applicant object
        """
        try:
            applicant_id = uuid.uuid4()
            applicant = Applicant(first_name = f_name, last_name = l_name, email = email, applicant_id = str(applicant_id))
            self._session.add(applicant)
            self._session.commit()
            self._session.refresh(applicant)
            return applicant
        except (InvalidRequestError, NoResultFound) as err:
            self._session.rollback()
            print(err)
            return None

    def add_recruiter(self, email, full_name) -> Recruiter:
        """ This method adds a recruiter to the db
        Return: Returns the new recruiter object
        """
        try:
            recruiter_id = uuid.uuid4()
            recruiter = Recruiter(full_name = full_name, email = email, recruiter_id = str(recruiter_id))
            self._session.add(recruiter)
            self._session.commit()
            self._session.refresh(recruiter)
            return recruiter
        except (InvalidRequestError, NoResultFound) as err:
            self._session.rollback()
            print(err)
            return None
    def add_vacancy(self, j_title, dept, unit, l_manager, no_open_pos,
    date_of_req, bp, location, jd_summary) -> Vacancy:
        """ This method adds a Vacancy to the db
        Return: Returns the new vacancy object
        """
        try:
            job_id = uuid.uuid4()

            vacancy = Vacancy(job_title = j_title, department = dept, unit = unit, line_manager = l_manager, 
            job_id = str(job_id), number_of_open_positions = no_open_pos, date_of_requisition = date_of_req,
            business_partner = bp, location = location, job_description_summary = jd_summary)

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
        applicant = self.find_applicant_by(applicant_id=applicant_id)
        for key, value in kwargs.items():
            if not hasattr(Applicant, key):
                raise ValueError
            else:
                setattr(applicant, key, value)
        self._session.commit()
        return None

    def update_recruiter(self, recruiter_id, **kwargs) -> None:
        """ This method updates recruiters table based on id
        @recruiter_id: recruiter Id to be found
        Return: Returns none
        """
    def update_vacancy(self, job_id, **kwargs) -> None:
        """ This method updates vacancy table based on id
        @job_id: job Id to be found
        Return: Returns none
        """
        vacancy = self.find_vacancy_by(job_id=job_id)
        for key, value in kwargs.items():
            if not hasattr(Vacancy, key):
                raise ValueError
            else:
                setattr(vacancy, key, value)
        self._session.commit()
        return None

    def add_applications(self, applicant_id, job_id):
        """ This function logs every application in the applicants_vacancy table
        """
        try:
            application = ApplicantsVacancy(applicant_id = applicant_id, job_id=job_id)
            self._session.add(application)
            self._session.commit()
            print("You have a new application")
            return application
        except (InvalidRequestError, NoResultFound) as err:
            self._session.rollback()
            print(err)
            return None