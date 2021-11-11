from flask_sqlalchemy import SQLAlchemy
import requests
from app import db
from app import Email
import urllib.request
import random
import time
import os
from datetime import datetime
from unidecode import unidecode

emails = Email.query.all()
for email in emails:
    email.day_age = email.day_age + 1
    db.session.add(email)
    db.session.commit()
