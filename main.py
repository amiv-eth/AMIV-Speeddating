####!/usr/bin/env python3

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
#from apps.database import db
#from apps.models import Participants, TimeSlots
import requests

import datetime
year = datetime.datetime.now().year

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:toor@localhost/Speeddating'
db = SQLAlchemy(app)

class Participants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    DefSlot = db.Column(db.Integer, primary_key=False)
    AvailableSlot = db.Column(db.String(50), primary_key=False)
    Name = db.Column(db.String(80), unique=False)
    Prename = db.Column(db.String(80), unique=False)
    EMail = db.Column(db.String(120), unique=False)
    MobileNr = db.Column(db.String(20), unique=False)
    Address = db.Column(db.String(200), unique=False)
    Age = db.Column(db.Integer, unique=False)
    Sexe = db.Column(db.Boolean, unique=False)
    EventYear = db.Column(db.Integer, unique=False)
    StudyCourse = db.Column(db.String(80), unique=False)
    StudySemester = db.Column(db.String(80), unique=False)
    PerfectDate = db.Column(db.String(300), unique=False)
    SingleSince = db.Column(db.String(80), unique=False)
    OnlineDating = db.Column(db.String(300), unique=False)
    PickupLine = db.Column(db.String(300), unique=False)
    Women = db.Column(db.String(300), unique=False)
    Men = db.Column(db.String(300), unique=False)
    Advantages = db.Column(db.String(300), unique=False)
    NrDates = db.Column(db.String(300), unique=False)
    LongestRelationship = db.Column(db.String(300), unique=False)
    FindDates = db.Column(db.String(300), unique=False)
    Fruit = db.Column(db.String(300), unique=False)

    def __init__(self, name, prename, email, mobileNr, address, age, sexe, year=None, dSlot=None, aSlot=None, course=None, semester=None, perfDate=None, singleSince=None, onlineDating=None, pickup=None, women=None, men=None, advantages=None, nrDates=None, longestRel=None, findDates=None, fruit=None):
        self.DefSlot = dSlot
        self.AvailableSlot = aSlot
        self.Name = name
        self.Prename = prename
        self.EMail = email
        self.MobileNr = mobileNr
        self.Address = address
        self.Age = age
        self.Sexe = sexe
        self.EventYear = year
        self.StudyCourse = course
        self.StudySemester = semester
        self.PerfectDate = perfDate
        self.SingleSince = singleSince
        self.OnlineDating = onlineDating
        self.PickupLine = pickup
        self.Women = women
        self.Men = men
        self.Advantages = advantages
        self.NrDates = nrDates
        self.LongestRelationship = longestRel
        self.FindDates = findDates
        self.Fruit = fruit

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
