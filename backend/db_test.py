from db import DB
import datetime

new_db = DB()

new_db.add_applicant("Nimi", "Williams", "Williamson.nimi@gmail.com")
applicant = new_db.find_applicant_by(first_name="Nimi")
print(applicant.first_name)

new_db.update_applicant(applicant.applicant_id, first_name="Murray")
print(applicant.first_name)

jd_summary = " This job involves understanding recruitment requirments and doing the needful in bringing in the best talent"
date = datetime.datetime.now()

new_db.add_vacancy("Senior Technical Recruiter", "Human Capital", "Talent Acqquisition", "Williams Nimi", 2, date, "Sandra Emerenwan", "Lagos", jd_summary)
vacancy = new_db.find_vacancy_by(job_title = "Senior Technical Recruiter")
print(vacancy.business_partner)

new_db.update_vacancy(vacancy.job_id, business_partner="Nimi Williams")
print(vacancy.business_partner)