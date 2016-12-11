#!/usr/bin/env python3

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from apps.models import Participants, TimeSlots
import requests
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:toor@localhost/Speeddating'
db = SQLAlchemy(app)

# Creates tables only when they don't already exist so we can just leave this here
db.create_all()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        result = request.form

        # Send POST request with parameters 'username' and 'password'. Verification has to be off since
        # SSL certs are self-signed.
        ack = requests.post("https://amiv-apidev.vsos.ethz.ch/sessions", data={"username" : str(result['nethz']), "password" : str(result['password'])}, verify=False)

        if ack.status_code == 201:
            return render_template("admin.html")
        return render_template('login.html')
    return render_template('login.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        try:
            year = datetime.datetime.now().year
            result = request.form
            prename = str(result['prename'])
            name = str(result['name'])
            mobile = str(result['mobile'])
            address = str(result['address'])
            email = str(result['mail'])
            age = int(result['age'])
            gender = bool(result['gender'])

        except Exception as e:
            print(e)

            # TODO: Show actual error instead of redirectiing to an error page
            return render_template('error.html')

        admin = Participants(name, prename, email, mobile, address, age, gender, year)
        db.session.add(admin)
        db.session.commit()

        return render_template('success.html')

    return render_template('signup.html')



if __name__ == '__main__':
    app.run()
