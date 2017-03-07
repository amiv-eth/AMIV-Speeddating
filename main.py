#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from apps.models import Participants, TimeSlots
import requests
import datetime
from flask.ext.login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

# create and config app
app = Flask(__name__)
app.config.from_pyfile("./apps/config.py")
app.secret_key = app.config['APP_SECRET']
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI']
db = SQLAlchemy(app)

# Creates tables only when they don't already exist so we can just leave this here
db.create_all()

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    if username not in app.config['USERS'].keys():
        return

    user = User()
    user.id = username
    return user



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    form_username = request.form['username']
    if form_username in app.config['USERS'].keys():
        if app.config['USERS'][form_username] == request.form['password']:
            user = User()
            user.id = form_username
            login_user(user)
            return redirect(url_for('admin'))
    return 'Bad login'


@app.route('/logout')
def logout():
    logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


@app.route('/admin', methods=["GET", "POST"])
@login_required
def admin():
    #return 'Logged in as: ' + current_user.id
    return render_template('admin.html')


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
