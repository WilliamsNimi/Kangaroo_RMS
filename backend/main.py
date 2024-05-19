from db import DB
import datetime
from applicant import Applicant
from recruiter import Recruiter
from bp import BusinessPartner

new_db = DB()

# Class Instantiation
recruiter = Recruiter()
bp = BusinessPartner()
applicant = Applicant()


#Create a new Recruiter, Business Partner and Applicant
new_recruiter = recruiter.create_recruiter(new_db, "Nimi.williams@sterling.ng", "Nimi Williams")
new_bp = bp.create_business_partner(new_db, "Joshua.agbeke@sterling.ng", "Joshua Agbeke")
new_applicant = applicant.create_applicant(new_db, "John", "Farnam", "JohnFarnam@sterling.ng")


#new_bp makes a requisition
job_title = "Technical Recruiter"
department = "Human Capital"
unit = "Talent Acquisition"
line_manager = "Awosika Afolayan"
number_of_open_positions = 2
location = "Lagos"
job_description_summary = "Lorem ipsom ipsom dolor sit amet"
new_vacancy = bp.make_requisition(new_db, job_title, department, unit, line_manager, number_of_open_positions, location, job_description_summary)
print(new_vacancy.approval_status)

#Recruiter approves the new vacancy by changing the status to Approved
recruiter.update_vacancy(new_db, new_vacancy.job_id, approval_status="Approved")
print(new_vacancy.approval_status)

print(new_db.show_all_vacancies())
print(new_db.show_all_bps())
print(new_db.show_all_recruiters())
print(new_db.show_all_applicants())


