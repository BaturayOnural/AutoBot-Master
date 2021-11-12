from flask_sqlalchemy import SQLAlchemy
import requests
from app import db
from app import Task, Bot, Name, Surname
import urllib.request
import random
import time
import os
from datetime import datetime
from unidecode import unidecode

# Api keys + proxy matching
webshare_api_key = "3c43d9fc51d65c8cf7fe3bb85d1ecfcade8b41be"
proxies = []

response = requests.get("https://proxy.webshare.io/api/proxy/list/", headers={"Authorization": webshare_api_key}).json()

for elem in response.get("results"):
    IP = elem.get("proxy_address")
    PORT = str(elem.get("ports").get("http"))
    PROXY = IP + ":" + PORT
    #PROXY = "https:\/\/" + PROXY
    print(PROXY)
    proxies.append(PROXY)

def get_random_name(gender_proposed):
    names = Name.query.filter_by(gender=gender_proposed).all()
    name = random.choice(names)
    return str(unidecode(name.name))

def get_random_surname():
    surnames = Surname.query.all()
    surname = random.choice(surnames)
    return str(unidecode(surname.surname))

def fire_event(bot, task):
    bot = Bot.query.get(bot)
    bot_ip = bot.digital_ocean_ip
    bot_proxy = proxies[int(bot.id) - 1]
    url = 'http://' + bot_ip + '/email' + '/' +  bot_proxy + '/' + str(task.id) + '/' + get_random_name(random.choice(['E','K'])) + '/' + get_random_surname()
    resp = requests.get(url)

def kill_email(bot):
    bot = Bot.query.get(bot)
    bot_ip = bot.digital_ocean_ip
    url = 'http://' + bot_ip + '/kill_email'
    resp = requests.get(url)

tasks = Task.query.filter_by(status="Started").all()
for task in tasks:
    if ((int(task.target) - int(task.success)) >= len(task.bots.split(","))):
        task.attempts = str(int(task.attempts) + len(task.bots.split(",")))
        bots = task.bots.split(",")
        for bot in bots:
            kill_email(bot)
        time.sleep(3)
        for bot in bots:
            fire_event(bot, task)
    elif((int(task.target) - int(task.success)) > 0):
        task.attempts = str(int(task.attempts) + (int(task.target) - int(task.success)))
        bots = task.bots.split(",")
        bots = random.sample(bots, (int(task.target) - int(task.success)))
        for bot in bots:
            kill_email(bot)
        time.sleep(3)
        for bot in bots:
            fire_event(bot, task)
    else:
        task.status = "Completed"
        task.finish = datetime.now()
        bots = task.bots.split(",")
        for bot in bots:
            bot = Bot.query.get(bot)
            bot.status = "Idle"
            db.session.add(bot)
            db.session.commit()
    db.session.add(task)
    db.session.commit()
