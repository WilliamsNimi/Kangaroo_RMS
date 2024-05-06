#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from model import Base, Applicant, Recruiter, Vacancy, ApplicantsVacancy


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

    def add_applicant(self) -> Applicant:
        """ This method adds an applicant to the db
        Return: Returns the new applicant object
        """
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
