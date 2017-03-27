#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

from app.forms import LoginForm, CreateEventForm, CreateTimeSlotForm, SignupForm
from app.models import Participants, TimeSlots, Events
#from app.tables import Participants, TimeSlots, Events
from app.functions import event_change_signup_status, event_change_active_status

# create and config app
app = Flask(__name__)
app.config.from_pyfile("./app/config.py")
app.secret_key = app.config['APP_SECRET']

# create DB connection
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)            
                       
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
    return redirect(url_for('admin'))

# unauthorized handler redirecting to index
@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect('/')


# protected admin overview page
@app.route('/admin', methods=["GET", "POST"])
@login_required
def admin():
    events = None
    if request.method == 'GET':
        session = Session()
        try:
            events = session.query(Events).all()
        except Exception as e:
            session.rollback()
            print(e)
            # TODO: Show actual error instead of redirectiing to an error page
            return render_template('error.html')
        finally:
            session.close()
    return render_template('admin.html', events=events)

# protected admin event view page
@app.route('/event_view/<int:event_id>', methods=["GET", "POST"])
@login_required
def event_view(event_id):
    if request.method == 'GET':
        eventid = event_id
        slots = None
        eventname = None
        session = Session()
        try:
            slots = session.query(TimeSlots).filter(TimeSlots.EventID==event_id)
            event = session.query(Events).filter(Events.ID==event_id).first()
        except Exception as e:
            session.rollback()
            print(e)
            # TODO: Show actual error instead of redirectiing to an error page
            return render_template('error.html')
        finally:
            session.close()    
        return render_template('event_view.html', eid = eventid, slots=slots, event=event)

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
            timestamp = datetime.now()
            signup_open = 0
            active = 0
        
        except Exception as e:
            print(e)
            # TODO: Show actual error instead of redirectiing to an error page
            return render_template('error.html')

        session = Session()
        try:
            event = Events(name, year, semester, timestamp, signup_open, active)
            session.add(event)
            session.commit()
        except Exception as e:
            session.rollback()
            print(e)
            # TODO: Show actual error instead of redirectiing to an error page
            return render_template('error.html')
        finally:
            session.close()
        return redirect(url_for('admin'))
    return render_template('create_event.html', form=form)


# protected admin create new timeslot of an event page
@app.route('/create_timeslot/<int:event_id>', methods=["GET", "POST"])
@login_required
def create_timeslot(event_id):
    form = CreateTimeSlotForm(request.form)
    eventid = event_id
    if request.method == 'POST' and form.validate():
        session = Session()
        try:
            date = str(request.form['date'])
            starttime = str(request.form['starttime'])
            endtime = str(request.form['endtime'])
            nrcouples = int(request.form['nrcouples'])
            agerange = int(request.form['agerange'])
            slot = TimeSlots(eventid, date, starttime, endtime, nrcouples, agerange)
            session.add(slot)
            session.commit()
            
        except Exception as e:
            session.rollback()
            print(e)
            # TODO: Show actual error instead of redirectiing to an error page
            return render_template('error.html')

        finally:
            session.close()
        
        return redirect(url_for('event_view', event_id = eventid))
    return render_template('create_timeslot.html', eid = eventid, form=form)

# link for open/cose the signup
@app.route('/change_signup/<int:event_id>/<int:open>', methods=["GET", "POST"])
@login_required
def change_signup(event_id, open):
    session = Session()
    try:
        changed = event_change_signup_status(session, event_id, open)
    except Exception as e:
        session.rollback()
        print(e)
        # TODO: Show actual error instead of redirectiing to an error page
        return render_template('error.html')
    finally:
        session.close()
    if changed:
        return redirect(url_for('admin'))
    return render_template('error.html')

# link for activate an event ## TODO merge to one single function
@app.route('/activate_event/<int:event_id>/<int:active>', methods=["GET", "POST"])
@login_required
def activate_event(event_id, active):
    session = Session()
    try:
        activated = event_change_active_status(session, event_id, active)
    except Exception as e:
        session.rollback()
        print(e)
        # TODO: Show actual error instead of redirectiing to an error page
        return render_template('error.html')
    finally:
        session.close()
    if activated:
        return redirect(url_for('admin'))
    return render_template('error.html')



# signup page
@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignupForm(request.form)
    if request.method == 'GET':
        session = Session()
        try:
            event = session.query(Events).filter(Events.Active=='1').first()
            eventid = event.ID
            timeslots = session.query(TimeSlots).filter(TimeSlots.EventID==eventid).all()
            #if timeslots != None:
                #form.availableslots.choices = [(int(slot.ID), '&nbsp &nbsp ' + str(slot.Date.strftime("%A %d. %B %Y")) + '&nbsp &nbsp' + str(slot.StartTime)[:-3] + ' - ' + str(slot.EndTime)[:-3] + '&nbsp &nbsp &nbsp Altersgruppe: ' + str(slot.AgeRange)) for slot in timeslots]

        except Exception as e:
            session.rollback()
            print(e)
            # TODO: Show actual error instead of redirectiing to an error page
            return render_template('error.html')

        finally:
            session.close()
    return render_template('signup.html', form=form)
                
    if request.method == 'POST' and form.validate():
        session = Session()
        try:
            timestamp = datetime.datetime.now()
            #name = str(request.form['name'])
            #prename = str(request.form['prename'])
            #gender = int(request.form['gender'])
            #email = str(request.form['email'])
            #mobile = str(request.form['mobilenr'])
            #address = str(request.form['address'])
            #birthday = str(request.form['birthday'])
            #studycourse = str(request.form['studycourse'])
            #studysemester = str(request.form['studysemester'])
            #perfectdate = str(request.form['perfectdate'])
            #fruit = str(request.form['fruit'])
            #availableslots = int(request.form['availableslots'])
            
            #new_participant = Participants(timestamp, eventid, name, prename, email, mobile, address, birthday, gender, course=studycourse, semester=studysemester, perfDate=perfectdate, fruit=fruit, aSlot=availableslots)
            #session.add(new_participant)
            #session.commit()

        except Exception as e:
            session.rollback()
            print(e)
            # TODO: Show actual error instead of redirectiing to an error page
            return render_template('error.html')

        finally:
            session.close()

        return render_template('success.html')
    return render_template('signup.html', form=form)


if __name__ == '__main__':
    app.run()
