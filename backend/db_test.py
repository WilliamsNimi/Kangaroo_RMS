from db import DB
import datetime
from applicant import Applicant
from recruiter import Recruiter
from bp import BusinessPartner


new_db = DB()

new_db.add_applicant("Nimi", "Williams", "Williamson.nimi@gmail.com")

applicants = Applicant()
new_applicant = applicants.create_applicant("Nimi", "williams", "williamson.nimi@gmail.com")

bp = BusinessPartner()
new_bp = bp.create_business_partner("Nimi.williams@sterling.ng", "Nimi Williams")
print(new_bp.email)
new_req = bp.make_requisition("Technical Recruiter", "Talent Acquisition", "Recruitment", "Dipo Awojide", 2, "Lagos", "Bla bla bla")

jd_summary = " This job involves understanding recruitment requirments and doing the needful in bringing in the best talent"
date = datetime.datetime.now()
vacancy = new_db.find_vacancy_by(job_title = "Technical Recruiter")
applicants.apply(new_applicant.applicant_id, vacancy.job_id)

"""
new_db.update_applicant(applicant.applicant_id, first_name="Murray")
print(applicant.first_name)

jd_summary = " This job involves understanding recruitment requirments and doing the needful in bringing in the best talent"
date = datetime.datetime.now()

new_db.add_vacancy("Senior Technical Recruiter", "Human Capital", "Talent Acqquisition", "Williams Nimi", 2, date, "Sandra Emerenwan", "Lagos", jd_summary)
vacancy = new_db.find_vacancy_by(job_title = "Senior Technical Recruiter")
print(vacancy.business_partner)

new_db.update_vacancy(vacancy.job_id, business_partner="Nimi Williams")
print(vacancy.business_partner)

new_db.add_recruiter("nimi.williams@sterling.ng", "Nimi Williams")
recruiter = new_db.find_recruiter_by(email="nimi.williams@sterling.ng")
print(recruiter.recruiter_id)

new_db.add_applications(applicant.applicant_id, vacancy.job_id)


applicants = Applicant()
db = DB()

new_applicant = applicants.create_applicant("Nimi", "williams", "williamson.nimi@gmail.com")
print(new_applicant.first_name)
#db.update_applicant(applicant.applicant_id, first_name="Nimi", last_name="Murray")
print(new_applicant.applicant_id)
applicants.update_profile(new_applicant.applicant_id, first_name="Murray")
print(new_applicant.first_name)


recruiter = Recruiter()
new_recruiter = recruiter.create_recruiter("nimi.williams@sterling.ng", "Nimi Williams")
print(new_recruiter.email)
print(recruiter.update_profile(new_recruiter.recruiter_id, email="nimi.williams@yahoo.com"))
print(new_recruiter.email)

bp = BusinessPartner()
new_bp = bp.create_business_partner("Nimi.williams@sterling.ng", "Nimi Williams")
print(new_bp.email)
new_req = bp.make_requisition("Technical Recruiter", "Talent Acquisition", "Recruitment", "Dipo Awojide", 2, "Lagos", "Bla bla bla")
print(new_req.job_title)
"""