#!/usr/bin/env python3

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from apps.database import db
from apps.models import Participants, TimeSlots
import requests


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:toor@localhost/Speeddating'
    db.init_app(app)
    return app


app = create_app()


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
        admin = Participants(prename, name)
        db.session.add(admin)
        db.session.commit()
        return render_template('index.html')
    return render_template('signup.html')



if __name__ == '__main__':
   app.run()
