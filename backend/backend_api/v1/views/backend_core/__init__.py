from backend_core.applicant import Applicant
from backend_core.recruiter import Recruiter
from backend_core.bp import BusinessPartner
from backend_core.db import DB


print("Importing", __name__)

recruiter = Recruiter()
bp = BusinessPartner()
applicant = Applicant()
db = DB()