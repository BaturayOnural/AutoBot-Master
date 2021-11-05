from flask_sqlalchemy import SQLAlchemy
from app import db
from app import Task, Bot
import urllib.request

tasks = Task.query.filter_by(status="Started").all()

for task in tasks:
    if (task.status == "Started"):
         if ((task.target - task.success) > len(task.bots_array)):
             task.attempts = str(int(task.attempts) + len(task.bots_array)
             bots = task.bots_array
             for bot in bots:
                 bot_obj = Bot.query.get(int(bot))
                 bot_ip = bot_obj.digital_ocean_ip
                 url = 'http://' + bot_ip + '/' + set_status + ' # status update
                 resp = requests.get(url)
         else:
             task.attempts = str(int(task.attempts) + (task.target - task.success))
