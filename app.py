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

# Init Database
db = SQLAlchemy(app)

# Init Marshmallow
ma = Marshmallow(app)

# Email Model
class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(30))
    day_age = db.Column(db.Integer, default=0)

    def __init__(self, email_address, password, day_age):
            self.email_address = email_address
            self.password = password
            self.day_age = day_age

# Name Model
class Name(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), unique=True)
    last_name = db.Column(db.String(30), unique=True)
    gender = db.Column(db.String(10))

    def __init__(self, first_name, last_name, gender):
            self.first_name = first_name
            self.last_name = last_name
            self.gender = gender

# Bot Model
class Bot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))
    port = db.Column(db.String(10))
    proxy_ip = db.Column(db.String(30))
    digital_ocean_ip = db.Column(db.String(30))
    status = db.Column(db.String(10))

    def __init__(self, username, password, port, proxy_ip, digital_ocean_ip, status):
            self.username = username
            self.pasword = password
            self.port = port
            self.proxy_ip = proxy_ip
            self.digital_ocean_ip = digital_ocean_ip
            self.status = status

# Email Schema
class EmailSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email_address', 'password', 'day_age')

# Name Schema
class NameSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'gender')

# Bot Schema
class BotSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'port', 'proxy_ip', 'digital_ocean_ip')

# Init Schema
email_schema = EmailSchema()
emails_schema = EmailSchema(many=True)

name_schema = NameSchema()
names_schema = NameSchema(many=True)

bot_schema = BotSchema()
bots_schema = BotSchema(many=True)

# Additional routes for favicon and profile picture
@app.route('/templates/static/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'templates/static'),
                               'favicon.ico')

@app.route('/templates/static/ms.jpg')
def msoydan():
    return send_from_directory(os.path.join(app.root_path, 'templates/static'),
                               'ms.jpg')

# Casual routes for pages
@app.route('/overview')
def overview():
    return render_template("overview.html")

@app.route('/create_task')
def create_task():
    return render_template("create_task.html")

@app.route('/task_reports')
def task_reports():
    return render_template("task_reports.html")

@app.route('/database')
def database():
    return render_template("database.html")

@app.route('/bot_settings')
def bot_settings():
    return render_template("bot_settings.html")

@app.route('/')
def get_emails():
    return jsonify({'msg':"message"})

# Run server from terminal
if __name__ ==  "__main__":
    app.run(debug=True)
