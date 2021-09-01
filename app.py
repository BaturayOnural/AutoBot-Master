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

# Product Class/Model
class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, primary_key=True)

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
