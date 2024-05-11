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
            return applicant
        except (InvalidRequestError, NoResultFound) as err:
            self._session.rollback()
            print(err)
            return None

    def add_recruiter(self) -> Recruiter:
        """ This method adds a recruiter to the db
        Return: Returns the new recruiter object
        """
    def add_vacancy(self) -> Vacancy:
        """ This method adds a Vacancy to the db
        Return: Returns the new vacancy object
        """

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
    def find_vacancy_by(self, **kwargs) -> Vacancy:
        """ A method to search the db
        @query_str: the query to search for
        Return: Returns the first row where the vacancy is found
        """

    def update_applicant(self, applicant_id: int, **kwargs) -> None:
        """ This method updates applicants table based on id
        @applicant_id: user Id to be found
        Return: Returns none
        """
    def update_recruiter(self, recruiter_id: int, **kwargs) -> None:
        """ This method updates recruiters table based on id
        @recruiter_id: recruiter Id to be found
        Return: Returns none
        """
    def update_vacancy(self, job_id: int, **kwargs) -> None:
        """ This method updates vacancy table based on id
        @job_id: job Id to be found
        Return: Returns none
        """
