from db import DB

new_db = DB()

new_db.add_applicant("Nimi", "Williams", "Williamson.nimi@gmail.com")
print(new_db.find_applicant_by(first_name="Nimi"))