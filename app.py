from flask import Flask, render_template, send_from_directory, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import request
from flask_cors import CORS
import random
import requests
import os

# Api keys
webshare_api_key = "3c43d9fc51d65c8cf7fe3bb85d1ecfcade8b41be"

## construct ip list
# globals
#IP = ""
#PORT = ""
#PROXY = IP + ":" + PORT
#status = "0"

#response = requests.get("https://proxy.webshare.io/api/proxy/list/", headers={"Authorization": webshare_api_key})
#response = response.json()

#for elem in response.get("results"):
#    IP = elem.get("proxy_address")
#    PROXY = elem.get("ports").get("http")

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
CORS(app)

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
    name = db.Column(db.String(30), unique=True)
    gender = db.Column(db.String(10))

    def __init__(self, name, gender):
            self.name = name
            self.gender = gender

# Name Model
class Surname(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    surnaname = db.Column(db.String(30), unique=True)

    def __init__(self, surnamename):
            self.surname = name


# Bot Model
class Bot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(5))
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

# Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    instaId = db.Column(db.String(30))
    targetInstaId = db.Column(db.String(30))
    status = db.Column(db.String(30))
    target = db.Column(db.String(30))
    attempts = db.Column(db.String(30))
    type = db.Column(db.String(30))
    bots = db.Column(db.String(30))
    success = db.Column(db.String(30))
    bots_array = []

    def __init__(self, instaId, targetInstaId, status, target, attempts, type, bots, success):
            self.instaId = instaId
            self.targetInstaId = targetInstaId
            self.status = status
            self.target = target
            self.attempts = attempts
            self.type = type
            self.bots = bots
            self.success = success
            self.bots_array = []

# Email Schema
class EmailSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email_address', 'password', 'day_age')

# Name Schema
class NameSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'gender')

# Surname Schema
class SurnameSchema(ma.Schema):
    class Meta:
        fields = ('id', 'surname')

# Bot Schema
class BotSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'port', 'proxy_ip', 'digital_ocean_ip', 'status')

# Task Schema
class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'instaId', 'targetInstaId', 'status', 'target', 'attempts', 'type', 'bots', 'success')

# Init Schema
email_schema = EmailSchema()
emails_schema = EmailSchema(many=True)

name_schema = NameSchema()
names_schema = NameSchema(many=True)

surname_schema = SurnameSchema()
surnames_schema = SurnameSchema(many=True)

bot_schema = BotSchema()
bots_schema = BotSchema(many=True)

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

# Additional routes for favicon, profile picture, login background
@app.route('/templates/static/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'templates/static'),
                               'favicon.ico')

@app.route('/templates/static/ms.jpg')
def msoydan():
    return send_from_directory(os.path.join(app.root_path, 'templates/static'),
                               'ms.jpg')

@app.route('/templates/static/login_background.jpg')
def login_background():
    return send_from_directory(os.path.join(app.root_path, 'templates/static'),
                               'login_background.jpg')

# Casual routes for pages
@app.route('/overview')
def overview():
    bots_query = Bot.query.all()
    tasks = Task.query.all()
    for task in tasks:
        task.bots_array = task.bots.split(",")
    bots_occupied = Bot.query.filter_by(status="Occupied").all()
    bot_ids = []
    bot_ips = []
    for bot in bots_occupied:
        bot_ids.append(bot.id)
        bot_ips.append(bot.digital_ocean_ip)
    return render_template("overview.html", bots_occupied=bots_occupied, num_bots=len(bots_query), tasks=tasks, bot_ids=bot_ids, bot_ips=bot_ips)

@app.route('/create_task')
def create_task():
    bots_available = Bot.query.filter_by(status="Idle").all()
    print(bots_available)
    return render_template("create_task.html", bots_available=len(bots_available))

@app.route('/task_reports')
def task_reports():
    return render_template("task_reports.html")

@app.route('/database')
def database():
    return render_template("database.html")

@app.route('/login', methods = ["POST","GET"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email != "msoydan@autobot.com" and password != "msoydan123*":
            error_while_logging = '1'
            print("false login")
            return render_template("login.html", error_while_logging=error_while_logging)
        else:
            return overview()
    else:
        return render_template("login.html")

@app.route('/bot_settings')
def bot_settings():
    bots = Bot.query.all()
    response = requests.get("https://proxy.webshare.io/api/subscription/", headers={"Authorization": webshare_api_key})
    response = response.json()
    proxy_count = response['proxy_count']

    # use when creating task for proxy information
    response_refresh = requests.get("https://proxy.webshare.io/api/proxy/replacement/info/", headers={"Authorization": webshare_api_key})
    response_refresh = response_refresh.json()
    print(response_refresh['automatic_refresh_next_at'])
    response = requests.get("https://proxy.webshare.io/api/proxy/list/", headers={"Authorization": webshare_api_key})
    response = response.json()
    usernames = []
    passwords = []
    proxy_addresses = []
    ports = []
    for elem in response['results']:
        username = elem['username']
        password = elem['password']
        proxy_address = elem['proxy_address']
        port = elem['ports']['http']

        usernames.append(username)
        passwords.append(password)
        proxy_addresses.append(proxy_address)
        ports.append(port)

    return render_template("bot_settings.html", bots=bots, num_bots=len(bots), proxy_count=proxy_count)

# Routes for db model creation/update/delete
@app.route('/add_bot', methods=['POST'])
def add_bot():
        username = ""
        password = ""
        port = ""
        proxy_ip = ""
        digital_ocean_ip = request.form['digital_ocean_ip']
        status = "Idle"

        new_bot = Bot(username, password, port, proxy_ip, digital_ocean_ip, status)

        db.session.add(new_bot)
        db.session.commit()

        return bot_settings()

@app.route('/delete_bot', methods=['POST'])
def delete_bot():
        bot_name = request.form['bot_name']
        bot_id = bot_name.split("-")[1]
        bot_to_delete = Bot.query.get(int(bot_id))

        db.session.delete(bot_to_delete)
        db.session.commit()

        return bot_settings()

@app.route('/add_task', methods=['POST'])
def add_task():
        instaId=""
        targetInstaId=""
        status="Started"
        account_amount=request.form['account_amount']
        target=account_amount
        attempts="0"
        bot_amount=request.form['bot_amount']
        text=""
        task_type=request.form['task_type']
        type=task_type
        bots=""
        success="0"

        # assign bots to the task
        bots_available = Bot.query.filter_by(status="Idle").all()
        bots_selected = random.sample(bots_available, k=int(bot_amount))

        for elem in bots_selected:
            bots = bots + str(elem.id)
            bots = bots + ","

        bots = bots[:-1]
        new_task = Task(instaId, targetInstaId, status, target, attempts, type, bots, success)
        bots_split = bots.split(",")

        if task_type == "0":
            pass
        elif task_type == "1": # email
            for bot in bots_split:
                bot_to_change = Bot.query.get(int(bot))
                bot_to_change.status = "Occupied"
                db.session.add(bot_to_change)
                db.session.commit()
            db.session.add(new_task)
            db.session.commit()

        elif task_type == "2": # insta register
            pass
        elif task_type == "3": # task(comments etc)
            pass

        return overview()

# Run server from terminal
if __name__ ==  "__main__":
    app.run(debug=True)
