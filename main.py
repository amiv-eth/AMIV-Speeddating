#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from sqlalchemy import create_engine, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

from app.forms import LoginForm, CreateEventForm, CreateTimeSlotForm, SignupForm, ChangeDateNr
from app.models import Participants, TimeSlots, Events
from app.functions import event_change_signup_status, event_change_active_status, event_change_register_status, change_present, change_payed, change_datenr, export

# create and config app
app = Flask(__name__)
app.config.from_pyfile("./app/config.py")
app.secret_key = app.config['APP_SECRET']
#app.server_name = app.config['SERVER_NAME']

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
    session = Session()
    try:
        event = session.query(Events).filter(Events.Active=='1').first()
        if event != None:
            eventid = event.ID
            timeslots = session.query(TimeSlots).filter(TimeSlots.EventID==eventid).all()
            dates = list(set(list(slot.Date for slot in timeslots)))
        else:
            dates = None
        dates_string = ''
        if dates != None:
            for date in dates:
                dates_string = dates_string + str(date.strftime("%d. %B, "))
            dates_string = dates_string[:-2]
    except Exception as e:
        session.rollback()
        print(e)
        return render_template('error.html')
    finally:
        session.close()
    return render_template('index.html', event=event, dates=dates_string)


@app.route('/home')
def home():
    session = Session()
    try:
        event = session.query(Events).filter(Events.Active=='1').first()
        if event != None:
            eventid = event.ID
            timeslots = session.query(TimeSlots).filter(TimeSlots.EventID==eventid).all()
            dates = list(set(list(slot.Date for slot in timeslots)))
        else:
            dates = None
        dates_string = ''
        if dates != None:
            for date in dates:
                dates_string = dates_string + str(date.strftime("%d. %B, "))
            dates_string = dates_string[:-2]
    except Exception as e:
        session.rollback()
        print(e)
        return render_template('error.html')
    finally:
        session.close()
    return render_template('home.html', event=event, dates=dates_string)




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
            return render_template('error.html')
        finally:
            session.close()    
        return render_template('event_view.html', eid = eventid, slots=slots, event=event)

    
# protected admin event view page
@app.route('/event_participants/<int:event_id>', methods=["GET", "POST"])
@login_required
def event_participants(event_id):
    if request.method == 'GET':
        eid = event_id
        slots = None
        eventname = None
        women = []
        men = []
        inw = []
        inm = []
        mailinw = []
        mailoutw = []
        mailinm = []
        mailoutm = []
        
        session = Session()
        try:
            event = session.query(Events).filter(Events.ID==eid).first()
            slots = session.query(TimeSlots).filter(TimeSlots.EventID==eid)
            if slots != None:
            
                for slot in slots:
                    w = session.query(Participants).order_by((Participants.CreationTimestamp)).filter(Participants.EventID==eid, Participants.AvailableSlot==slot.ID, Participants.Gender == '1').all()
                    m = session.query(Participants).order_by((Participants.CreationTimestamp)).filter(Participants.EventID==eid, Participants.AvailableSlot==slot.ID, Participants.Gender == '0').all()
                    women.append(w)
                    men.append(m)
        except Exception as e:
            session.rollback()
            print(e)
            return render_template('error.html')
        finally:
            session.close()

    for wslot in women:
        inmail = ""
        outmail = ""
        wcount = 0
        for w in wslot:
            if w.Confirmed == 1 and wcount < 12:
                wcount = wcount + 1;
                inw.append(w.EMail)
                inmail = inmail + w.EMail + "; "
            else:
                outmail = outmail + w.EMail + "; "
            
        mailinw.append(inmail)
        mailoutw.append(outmail)
        
    for mslot in men:
        inmail = ""
        outmail = ""
        mcount = 0
        for m in mslot:
            if m.Confirmed == 1 and mcount < 12:
                mcount = mcount + 1;
                inm.append(m.EMail)
                inmail = inmail + m.EMail + "; "
            else:
                outmail = outmail + m.EMail + "; "
        mailinm.append(inmail)
        mailoutm.append(outmail)
                
    return render_template('event_participants.html', event = event, slots=slots, women=women, men=men, inw=inw, inm=inm, mailinw=mailinw, mailinm=mailinm, mailoutw=mailoutw, mailoutm=mailoutm)

        

    
# protected admin create new event page
@app.route('/create_event', methods=["GET", "POST"])
@login_required
def create_event():
    form = CreateEventForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            format = '%Y-%m-%dT%H:%M'
            name = str(request.form['name'])
            year = int(request.form['year'])
            semester = int(request.form['semester'])
            specialslot = int(request.form['specialslot'])
            specialslotname = str(request.form['specialslotname'])
            specialslotdescription = str(request.form['specialslotdescription'])
            timestamp = datetime.now()
            opensignuptimestamp = datetime.strptime(str(request.form['opensignuptimestamp']), format)
            closesignuptimestamp = datetime.strptime(str(request.form['closesignuptimestamp']), format)
            place = str(request.form['place'])
            participationfee = str(request.form['participationfee'])
            signup_open = 0
            active = 0
        
        except Exception as e:
            print(e)
            return render_template('error.html', message = str(request.form['opensignuptimestamp']))

        session = Session()
        try:
            event = Events(name, year, specialslot, specialslotname, specialslotdescription, semester, timestamp, signup_open, active, participationfee, opensignuptimestamp, closesignuptimestamp)
            session.add(event)
            session.commit()
        except Exception as e:
            session.rollback()
            print(e)
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
            return render_template('error.html')

        finally:
            session.close()
        
        return redirect(url_for('event_view', event_id = eventid))
    return render_template('create_timeslot.html', eid = eventid, form=form)


@app.route('/timeslot_view/<int:timeslot_id>', methods=["GET", "POST"])
@login_required
def timeslot_view(timeslot_id):
    if request.method == 'GET':
        slotid = timeslot_id
        participants = None
        inw = []
        inm = []
        
        session = Session()
        
        try:
            slot = session.query(TimeSlots).filter(TimeSlots.ID==slotid).first()
            women = session.query(Participants).order_by((Participants.CreationTimestamp)).filter(Participants.AvailableSlot==slotid, Participants.Gender == '1').all()
            men = session.query(Participants).order_by((Participants.CreationTimestamp)).filter(Participants.AvailableSlot==slotid, Participants.Gender == '0').all()
            event = session.query(Events).filter(Events.ID==slot.EventID).first()
        except Exception as e:
            session.rollback()
            print(e)
            return render_template('error.html')
        finally:
            session.close()

        mailinw = ""
        mailoutw = ""
        wcount = 0
        for w in women:
            if w.Confirmed == 1 and wcount < 12:
                wcount = wcount + 1;
                inw.append(w.EMail)
                mailinw = mailinw + w.EMail + "; "
            else:
                mailoutw = mailoutw + w.EMail + "; "
             
        mailinm = ""
        mailoutm = ""
        mcount = 0
        for m in men:
            if m.Confirmed == 1 and mcount < 12:
                mcount = mcount + 1;
                inm.append(m.EMail)
                mailinm = mailinm + m.EMail + "; "
            else:
                mailoutm = mailoutm + m.EMail + "; "
        
        return render_template('timeslot_view.html', event = event, slot=slot, women=women, men=men, inw=inw, inm=inm, mailinw=mailinw, mailinm=mailinm, mailoutw=mailoutw, mailoutm=mailoutm)


@app.route('/timeslot_view_ongoing/<int:timeslot_id>', methods=["GET", "POST"])
@login_required
def timeslot_view_ongoing(timeslot_id):
    form = ChangeDateNr(request.form)
    session = Session()
    csv=''

    if request.method == 'POST' and form.validate():
        session = Session()
        try:
            participant_id = int(request.form['participant_id'])
            datenr = int(request.form['datenr'])
            changed = change_datenr(session, participant_id, datenr)
            
        except Exception as e:
            #session.rollback()
            print(e)
            return render_template('error.html')

        finally:
            session.close()
    # "GET":                       
    try:
        slot = session.query(TimeSlots).filter(TimeSlots.ID==timeslot_id).first()
        women = session.query(Participants).order_by((Participants.CreationTimestamp)).filter(Participants.AvailableSlot==timeslot_id, Participants.Gender == '1', Participants.Present == '1').all()
        men = session.query(Participants).order_by((Participants.CreationTimestamp)).filter(Participants.AvailableSlot==timeslot_id, Participants.Gender == '0', Participants.Present == '1').all()
        event = session.query(Events).filter(Events.ID==slot.EventID).first()
    except Exception as e:
        session.rollback()
        print(e)
        return render_template('error.html')
    finally:
        session.close()
    form.datenr.data=''                  
    return render_template('timeslot_view_ongoing.html', event = event, slot=slot, women=women, men=men, form=form, csv=csv)



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
        return render_template('error.html')
    finally:
        session.close()
    if activated:
        return redirect(url_for('admin'))
    return render_template('error.html')

# link for register/deregister an participant ## TODO merge to one single function
@app.route('/register_participant/<int:event_id>/<int:participant_id>/<int:register>', methods=["GET", "POST"])
@login_required
def register_participant(event_id, participant_id, register):
    session = Session()
    try:
        registered = event_change_register_status(session, participant_id, register)
    except Exception as e:
        session.rollback()
        print(e)
        return render_template('error.html')
    finally:
        session.close()
    if registered:
        return redirect(url_for('event_participants', event_id = event_id))
    return render_template('error.html')


@app.route('/change_participant_on_timeslot/<int:slot_id>/<int:participant_id>/<string:action>', methods=["GET", "POST"])
@login_required
def change_participant_on_timeslot(slot_id, participant_id, action):
    session = Session()
    try:
        if action == 'present':
            changed = change_present(session, slot_id, participant_id)
        elif action == 'payed':
            changed = change_payed(session, slot_id, participant_id)
    except Exception as e:
        session.rollback()
        print(e)
        return render_template('error.html')
    finally:
        session.close()
    if changed:
        return redirect(url_for('timeslot_view', timeslot_id = slot_id))
    return render_template('error.html', message = 'changing '+ action + ' did not work. Maybe a participant wanted to pay before being present on event.' )


# signup page
@app.route('/signup', methods=["GET", "POST"])
def signup():
    session = Session()
    form = SignupForm(request.form)
    try:
        event = session.query(Events).filter(Events.Active=='1').first()
        if event != None:
            eventid = event.ID
            timeslots = session.query(TimeSlots).filter(TimeSlots.EventID==eventid).all()
            if timeslots != None:
                age_strings=[]
                age_strings.append('< 22'.ljust(6))
                age_strings.append('22-25'.ljust(6))
                age_strings.append('> 25'.ljust(6))

                ids = []
                strings = []
                for s in timeslots:
                    ids.append(int(s.ID))
                    women = session.query(Participants).filter(Participants.AvailableSlot==s.ID, Participants.Confirmed=='1', Participants.Gender == '1').count()
                    men = session.query(Participants).filter(Participants.AvailableSlot==s.ID, Participants.Confirmed=='1', Participants.Gender == '0').count()
                    stri = '&nbsp &nbsp '
                    stri = stri + s.Date.strftime("%a %d. %B %Y") + '&nbsp &nbsp '
                    stri = str(stri).ljust(50,' '[0:1]) + str(s.StartTime)[:-3] + ' - ' + str(s.EndTime)[:-3]
                    stri = stri + '&nbsp &nbsp '
                    stri = stri + 'Altersgruppe: &nbsp' + age_strings[s.AgeRange]
                    stri = stri + '&nbsp &nbsp # angemeldete Personen: &nbsp &nbsp  M: ' + str(men)
                    stri = stri + '&nbsp &nbsp W: ' + str(women)
                    strings.append(stri)
                    
                

                form.availableslots.choices = [(ids[i], strings[i]) for i in range(0,len(timeslots))]
                
                #form.availableslots.choices = [(int(slot.ID), '&nbsp &nbsp ' + str(slot.Date.strftime("%A %d. %B %Y")) + '&nbsp &nbsp' + str(slot.StartTime)[:-3] + ' - ' + str(slot.EndTime)[:-3] + '&nbsp &nbsp &nbsp Altersgruppe: &nbsp' + age_strings[slot.AgeRange]) for slot in timeslots]                 
                                                      
    except Exception as e:
        #session.rollback()
        print(e)
        return render_template('error.html')
                            
    if request.method == 'POST' and form.validate():
        try:
            timestamp = datetime.now()
            name = str(request.form['name'])
            prename = str(request.form['prename'])
            gender = int(request.form['gender'])
            email = str(request.form['email'])
            mobile = str(request.form['mobilenr'])
            address = str(request.form['address'])
            birthday = str(request.form['birthday'])
            studycourse = str(request.form['studycourse'])
            studysemester = str(request.form['studysemester'])
            perfectdate = str(request.form['perfectdate'])
            fruit = str(request.form['fruit'])
            availableslots = int(request.form['availableslots'])
            confirmed = 1
            present = 0
            payed = 0

            bday= datetime.strptime(birthday, '%d.%m.%Y')

            count = session.query(Participants).filter(Participants.EMail==email, Participants.EventID==eventid).count()

            if count == 0:
                new_participant = Participants(timestamp, eventid, name, prename, email, mobile, address, bday, gender, course=studycourse, semester=studysemester, perfDate=perfectdate, fruit=fruit, aSlot=availableslots, confirmed=confirmed, present=present, payed=payed)
                session.add(new_participant)
                session.commit()
            else:
                message = 'Die E-Mail Adresse ' + email + ' wurde bereits für das Speeddating angewendet. Bitte versuchen Sie es erneut mit einer neuen E-Mail Adresse.'
                return render_template('error.html', message=message)

        except Exception as e:
            #session.rollback()
            print(e)
            return render_template('error.html')

        finally:
            session.close()
        return render_template('success.html')
    else:
        if session:
            session.close()
        
    return render_template('signup.html', form=form, event=event)




# manual signup page
@app.route('/manual_signup', methods=["GET", "POST"])
def manual_signup():
    session = Session()
    form = SignupForm(request.form)
    try:
        event = session.query(Events).filter(Events.Active=='1').first()
        if event != None:
            eventid = event.ID
            timeslots = session.query(TimeSlots).filter(TimeSlots.EventID==eventid).all()
            if timeslots != None:
                age_strings=[]
                age_strings.append('< 22'.ljust(6))
                age_strings.append('22-25'.ljust(6))
                age_strings.append('> 25'.ljust(6))

                ids = []
                strings = []
                for s in timeslots:
                    ids.append(int(s.ID))
                    women = session.query(Participants).filter(Participants.AvailableSlot==s.ID, Participants.Confirmed=='1', Participants.Gender == '1').count()
                    men = session.query(Participants).filter(Participants.AvailableSlot==s.ID, Participants.Confirmed=='1', Participants.Gender == '0').count()
                    stri = '&nbsp &nbsp '
                    stri = stri + s.Date.strftime("%a %d. %B %Y") + '&nbsp &nbsp '
                    stri = str(stri).ljust(50,' '[0:1]) + str(s.StartTime)[:-3] + ' - ' + str(s.EndTime)[:-3]
                    stri = stri + '&nbsp &nbsp '
                    stri = stri + 'Altersgruppe: &nbsp' + age_strings[s.AgeRange]
                    stri = stri + '&nbsp &nbsp # angemeldete Personen: &nbsp &nbsp  M: ' + str(men)
                    stri = stri + '&nbsp &nbsp W: ' + str(women)
                    strings.append(stri)
                    
                

                form.availableslots.choices = [(ids[i], strings[i]) for i in range(0,len(timeslots))]

                
    except Exception as e:
        #session.rollback()
        print(e)
        return render_template('error.html')
                            
    if request.method == 'POST' and form.validate():
        try:
            timestamp = datetime.now()
            name = str(request.form['name'])
            prename = str(request.form['prename'])
            gender = int(request.form['gender'])
            email = str(request.form['email'])
            mobile = str(request.form['mobilenr'])
            address = str(request.form['address'])
            birthday = str(request.form['birthday'])
            studycourse = str(request.form['studycourse'])
            studysemester = str(request.form['studysemester'])
            perfectdate = str(request.form['perfectdate'])
            fruit = str(request.form['fruit'])
            availableslots = int(request.form['availableslots'])
            confirmed = 1
            present = 1
            payed = 0

            bday= datetime.strptime(birthday, '%d.%m.%Y')

            count = session.query(Participants).filter(Participants.EMail==email, Participants.EventID==eventid).count()

            if count == 0:
                new_participant = Participants(timestamp, eventid, name, prename, email, mobile, address, bday, gender, course=studycourse, semester=studysemester, perfDate=perfectdate, fruit=fruit, aSlot=availableslots, confirmed=confirmed, present=present, payed=payed)
                session.add(new_participant)
                session.commit()
            else:
                message = 'Die E-Mail Adresse ' + email + ' wurde bereits für das Speeddating angewendet. Bitte versuchen Sie es erneut mit einer neuen E-Mail Adresse.'
                return render_template('error.html', message=message)

        except Exception as e:
            #session.rollback()
            print(e)
            return render_template('error.html')

        finally:
            session.close()
        return render_template('success.html')
    else:
        if session:
            session.close()
        
    return render_template('manual_signup.html', form=form, event=event)



# link for exporting the participants of a slot for the SpeedMatchTool
@app.route('/export_slot/<int:timeslot_id>', methods=["GET", "POST"])
@login_required
def export_slot(timeslot_id):
    session = Session()
    
    try:
        slot = session.query(TimeSlots).filter(TimeSlots.ID==timeslot_id).first()
        women = session.query(Participants).order_by((Participants.CreationTimestamp)).filter(Participants.AvailableSlot==timeslot_id, Participants.Gender == '1', Participants.Present == '1').all()
        men = session.query(Participants).order_by((Participants.CreationTimestamp)).filter(Participants.AvailableSlot==timeslot_id, Participants.Gender == '0', Participants.Present == '1').all()
        exported = export(women, men, slot)

    except Exception as e:
        session.rollback()
        print(e)
        return render_template('error.html')

    finally:
        session.close()

    if exported != '':
        return render_template('csv.html', slot=slot, exported=exported)
    return render_template('error.html')



if __name__ == '__main__':
    app.run()
