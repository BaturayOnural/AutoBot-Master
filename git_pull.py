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

def git_pull(bot):
    bot = Bot.query.get(bot)
    bot_ip = bot.digital_ocean_ip
    url = 'http://' + bot_ip + '/git_pull'
    resp = requests.get(url)

bots = Bot.query.all()
for bot in bots:
    git_pull(bot.id)
