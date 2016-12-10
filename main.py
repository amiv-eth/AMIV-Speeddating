#!/usr/bin/env python3

import pdb
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
#from apps.database import db
from apps.models import Participants, TimeSlots
import requests

import datetime
year = datetime.datetime.now().year

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:toor@localhost/Speeddating'
db = SQLAlchemy(app)


db.create_all()


prename = str("aoeu")
name = str("aoeu")
mobile = int("10")
address = str("aoeu")
email = str("aoeu")
gender = bool(1)
year = int(2016)
age = int(10)

admin = Participants(name, prename, mobile, address, email, gender, year, age)
db.session.add(admin)
db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        result = request.form
        ack = requests.post("https://amiv-apidev.vsos.ethz.ch/sessions", data={"user" : str(result['nethz']), "password" : str(result['password'])}, verify=False)
        if ack.status_code == 201:
            return render_template("admin.html")
        return render_template('login.html')
    return render_template('login.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        result = request.form
        prename = str(result['prename'])
        name = str(result['name'])
        mobile = str(result['mobile'])
        address = str(result['address'])
        email = str(result['mail'])
        age = int(result['age'])
        gender = bool(result['gender'])

        admin = Participants(name, prename, email, mobile, address, age, gender, year)
        db.session.add(admin)
        db.session.commit()
        return render_template('index.html')
    return render_template('signup.html')



if __name__ == '__main__':
   app.run()
