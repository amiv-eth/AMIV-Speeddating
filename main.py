#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from apps.forms import LoginForm, CreateEventForm, CreateTimeSlotForm
from apps.models import Participants, TimeSlots, Events
from apps.functions import change_signup_status, activate_event_status
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

# Create flask-login
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

# index page
@app.route('/')
def index():
    return render_template('index.html')

# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        fusername = request.form['username']
        if fusername in app.config['USERS'].keys():
            if app.config['USERS'][fusername] == request.form['password']:
                user = User()
                user.id = fusername
                login_user(user)
                return redirect(url_for('admin'))
            #return 'Bad login' TODO: return login error by validator wtform?
    return render_template('login.html', form=form)

# logout page
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out'

# unauthorized handler redirecting to index
@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect('/')


# protected admin overview page
@app.route('/admin', methods=["GET", "POST"])
@login_required
def admin():
    if request.method == 'GET':
        events = Events.query.all()
        return render_template('admin.html', events=events)

# protected admin event view page
@app.route('/event_view/<int:event_id>', methods=["GET", "POST"])
@login_required
def event_view(event_id):
    if request.method == 'GET':
        eventid = event_id
        slots = TimeSlots.query.filter_by(EventID=eventid).all()
        eventname = Events.query.filter_by(ID=eventid).first().Name
        return render_template('event_view.html', eid = eventid, slots=slots, eventname=eventname)

# protected admin create new event page
@app.route('/create_event', methods=["GET", "POST"])
@login_required
def create_event():
    form = CreateEventForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            name = str(request.form['name'])
            year = int(request.form['year'])
            semester = int(request.form['semester'])
            timestamp = datetime.datetime.now()
            signup_open = 0
            active = 0
        
        except Exception as e:
            print(e)
            # TODO: Show actual error instead of redirectiing to an error page
            return render_template('error.html')

        event = Events(name, year, semester, timestamp, signup_open, active)
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('create_event.html', form=form)


# protected admin create new timeslot of an event page
@app.route('/create_timeslot/<int:event_id>', methods=["GET", "POST"])
@login_required
def create_timeslot(event_id):
    form = CreateTimeSlotForm(request.form)
    eventid = event_id
    if request.method == 'POST' and form.validate():
        try:
            date = str(request.form['date'])
            starttime = str(request.form['starttime'])
            endtime = str(request.form['endtime'])
            nrcouples = int(request.form['nrcouples'])
            agerange = int(request.form['agerange'])
        
        except Exception as e:
            print(e)
            # TODO: Show actual error instead of redirectiing to an error page
            return render_template('error.html')

        slot = TimeSlots(eventid, date, starttime, endtime, nrcouples, agerange)
        db.session.add(slot)
        db.session.commit()
        return redirect(url_for('event_view', event_id = eventid))
    return render_template('create_timeslot.html', eid = eventid, form=form)

# link for open/cose the signup
@app.route('/change_signup/<int:event_id>/<int:open>', methods=["GET", "POST"])
@login_required
def change_signup(event_id, open):
    try:
        changed = change_signup_status(db, event_id, open)
    except Exception as e:
        print(e)
        # TODO: Show actual error instead of redirectiing to an error page
        return render_template('error.html')
    if changed:
        return redirect(url_for('admin'))
    return render_template('error.html')

# link for activate an event ## TODO merge to one single function
@app.route('/activate_event/<int:event_id>/<int:active>', methods=["GET", "POST"])
@login_required
def activate_event(event_id, active):
    try:
        activated = activate_event_status(db, event_id, active)
    except Exception as e:
        print(e)
        # TODO: Show actual error instead of redirectiing to an error page
        return render_template('error.html')
    if activated:
        return redirect(url_for('admin'))
    return render_template('error.html')



# signup page
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
