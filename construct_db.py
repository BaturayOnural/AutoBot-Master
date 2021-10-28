from flask_sqlalchemy import SQLAlchemy
from app import db
from app import Name, Surname

db.create_all()

file1 = open('./utility/isimler.txt', 'r')
Lines_names = file1.readlines()

# parse names and write db
count = 0
for line in Lines_names:
    tempstr = line.strip()
    tempstr = tempstr.strip("()")
    fields = tempstr.split(",")
    name = fields[0]
    gender = fields[1]
    name = name.strip("''")
    gender = gender.strip(" ")
    gender = gender.strip("''")
    new_name = Name(name, gender)
    db.session.add(new_name)
    db.session.commit()
    count += 1
print(count, end=" ")
print("names added in db.")

file1 = open('./utility/soyisimler.txt', 'r')
Lines_surnames = file1.readlines()

# parse surnames and write db
count = 0
for line in Lines_surnames:
    new_surname = line.strip()
    new_surname = Surname(new_surname)
    db.session.add(new_surname)
    db.session.commit()
    count += 1
print(count, end=" ")
print("surnames added in db.")
