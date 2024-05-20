import datetime
# from db import DB
# from applicant import Applicant
# from recruiter import Recruiter
# from bp import BusinessPartner


from backend_core import recruiter
from backend_core import db as new_db
from backend_core import applicant
from backend_core import bp


# new_db = DB()

# Class Instantiation
# recruiter = Recruiter()
# bp = BusinessPartner()
# applicant = Applicant()


#Create a new Recruiter, Business Partner and Applicant
new_recruiter = recruiter.create_recruiter("Nimi.williams@sterling.ng", "Nimi Williams")
new_bp = bp.create_business_partner("Joshua.agbeke@sterling.ng", "Joshua Agbeke")
new_applicant = applicant.create_applicant("John", "Farnam", "JohnFarnam@sterling.ng")


#new_bp makes a requisition
job_title = "Technical Recruiter"
department = "Human Capital"
unit = "Talent Acquisition"
line_manager = "Awosika Afolayan"
number_of_open_positions = 2
location = "Lagos"
job_description_summary = "Lorem ipsom ipsom dolor sit amet"
new_vacancy = bp.make_requisition(job_title, department, unit, line_manager, number_of_open_positions, location, job_description_summary)
print(new_vacancy.approval_status)

#Recruiter approves the new vacancy by changing the status to Approved
recruiter.update_vacancy(new_vacancy.job_id, approval_status="Approved", recruiter_id='9d6f5fe6-5e17-476e-92de-d23906a88a18')
print(new_vacancy.approval_status)

print(new_db.show_all_vacancies())
print(new_db.show_all_bps())
print(new_db.show_all_recruiters())
print(new_db.show_all_applicants())
print()
print()
print()
# try:
print(new_db.find_recruiter_vacancies_by('9d6f5fe6-5e17-476e-92de-d23906a88a18'))
print('IT WORKED IN MISSISSIPII')
# except Exception as e:
#     print('No vacancy found')
#     print()
#     print()
#     print(e)

