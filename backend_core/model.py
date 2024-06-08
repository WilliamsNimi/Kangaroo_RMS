#!/usr/bin/env python3
""" SQL Alchemy user model """
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, LargeBinary
Base = declarative_base()



class Applicant(Base):
    """ The Applicant Model class"""
    __tablename__ = 'applicants'
    id = Column(Integer, autoincrement=True)
    first_name = Column(String(250))
    last_name = Column(String(250))
    gender = Column(String(250))
    university = Column(String(250))
    course_of_study = Column(String(250))
    current_employer = Column(String(250))
    current_role = Column(String(250))
    years_of_experience = Column(String(250))
    salary_expectation = Column(Integer)
    other_relevant_information = Column(String(250))
    image = Column(LargeBinary)
    resume = Column(LargeBinary)
    applicant_id = Column(String(250), primary_key=True)
    email = Column(String(250))
    password = Column(String(250))
    phone_number = Column(String(250))

class Recruiter(Base):
    """ The Recruiter Model class"""
    __tablename__ = 'recruiters'
    id = Column(Integer, autoincrement=True)
    email = Column(String(250))
    password = Column(String(250))
    full_name = Column(String(250))
    job_role = Column(String(250))
    number_of_roles_assigned = Column(Integer)
    recruiter_id = Column(String(250), primary_key=True)

class Vacancy(Base):
    """ The Vacancy Model class"""
    __tablename__ = 'vacancy'
    id = Column(Integer, autoincrement=True)
    job_id = Column(String(250), primary_key=True)
    job_title = Column(String(250))
    department = Column(String(250))
    unit = Column(String(250))
    line_manager = Column(String(250))
    number_of_open_positions = Column(Integer)
    date_of_requisition = Column(DateTime)
    business_partner = Column(String(250))
    location = Column(String(250))
    job_description = Column(LargeBinary)
    job_description_summary = Column(String(250))
    recruiter_id = Column(String(250))
    requisition_id = Column(String(250))
    approval_status = Column(String(250))
    publish_status = Column(String(250))

class ApplicantsVacancy(Base):
    """ The Applicants_Vacancy bridge model class """
    __tablename__ = 'applicants_vacancy'
    id = Column(Integer, primary_key=True, autoincrement=True)
    applicant_id = Column(String(250))
    job_id = Column(String(250))

class BusinessPartner(Base):
    """ The Business Partner Model class """
    __tablename__ = 'business_partners'
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(250))
    email = Column(String(250))
    password = Column(String(250))