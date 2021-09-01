from flask import Flask, render_template, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init marshmallow
ma = Marshmallow(app)

# Email model
class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_adress = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(30))
    day_age = db.Column(db.Integer, default=0)

    def __init__(self, email_adress, password, day_age):
            self.email_adress = email_adress
            self.password = password
            self.day_age = day_age

# Name model
class Name(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), unique=True)
    last_name = db.Column(db.String(30), unique=True)
    gender = db.Column(db.String(10))

    def __init__(self, first_name, last_name, gender):
            self.first_name = first_name
            self.last_name = last_name
            self.gender = gender

# Bot model
class Bot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))
    port = db.Column(db.String(10))
    proxy_ip = db.Column(db.String(30))

    def __init__(self, username, password, port, proxy_ip):
            self.username = username
            self.pasword = password
            self.port = port
            self.proxy_ip = proxy_ip

# Email Schema
class EmailSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email_adress', 'pasword', 'day_age')

# Name Schema
class NameSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'gender')

# Bot Schema
class BotSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'port', 'proxy_ip')

# Additional routes for favicon and profile picture
@app.route('/templates/static/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'templates/static'),
                               'favicon.ico')

@app.route('/templates/static/ms.jpg')
def msoydan():
    return send_from_directory(os.path.join(app.root_path, 'templates/static'),
                               'ms.jpg')

# Casual routes
@app.route('/')
def index():
    return render_template("overview.html")

@app.route('/')
def get_emails():
    return jsonify({'msg':"message"})

# Run server from terminal
if __name__ ==  "__main__":
    app.run(debug=True)
