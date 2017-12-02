"""
Contains all views, i.e. anything that is routed to a url

"""

from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from app.models import Events, TimeSlots, Participants, AdminUser
from app.forms import LoginForm, CreateEventForm, CreateTimeSlotForm, SignupForm, DateNrChangeForm
from app.help_queries import get_string_of_date_list, get_list_women_of_slot, get_list_men_of_slot, get_string_mails_of_list
from app.functions import get_age, export, change_datenr, change_payed, change_present, event_change_register_status, event_change_active_status, event_change_signup_status
from app import app, db, login_manager, bcrypt, mail
from datetime import datetime
from flask_mail import Message
from app.signals import SIGNAL_NEW_SIGNUP
from app.participants import confirm_participation as _confirm_participation, cancel_participation as _cancel_participation


@app.route('/')
@app.route('/index')
def index():
    """ Index """
    try:
        event = Events.query.filter(Events.active == '1').first()
        dates = None
        if event != None:
            timeslots = TimeSlots.query.filter(
                TimeSlots.event_id == event.id).all()
            dates = list(set(list(slot.date for slot in timeslots)))
        dates_string = get_string_of_date_list(dates)
    except Exception as exception:
        print(exception)
        return render_template('error.html')
    return render_template('index.html', event=event, dates=dates_string)


@login_manager.user_loader
def get_admin_user(uid):
    """ Helper function for flask_login> """
    return AdminUser.query.filter_by(id=uid).first()


def check_credentials(username, password):
    """
    Looks for AdminUser with username, checks password
    Returns the AdminUser on success, else None
    """
    # Find the user in the database
    admin = AdminUser.query.filter_by(username=username).first()
    if admin is None:
        return None

    # Check password
    if bcrypt.check_password_hash(admin.password, password):
        return admin
    return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Login page to access admin pages """
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        fusername = request.form['username']
        fpassword = request.form['password']
        admin_user = check_credentials(fusername, fpassword)
        if admin_user is not None:
            login_user(admin_user)
            return redirect(url_for('admin'))
        else:
            render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """ Logout view """
    logout_user()
    return redirect(url_for('admin'))


@login_manager.unauthorized_handler
def unauthorized_handler():
    """ Catchall for unauthorized requests, redirect to index """
    return redirect('/')


@app.route('/admin', methods=["GET", "POST"])
@login_required
def admin():
    """ Admin overview page """
    events = None
    if request.method == 'GET':
        try:
            events = Events.query.all()
        except Exception as e:
            print(e)
            return render_template('error.html')
    return render_template('admin.html', events=events)


@app.route('/event_view/<int:event_id>', methods=["GET", "POST"])
@login_required
def event_view(event_id):
    """ Event list view """
    if request.method == 'GET':
        slots = None
        try:
            slots = TimeSlots.query.filter(TimeSlots.event_id == event_id)
            event = Events.query.filter(Events.id == event_id).first()
        except Exception as e:
            print(e)
            return render_template('error.html')
        return render_template('event_view.html', slots=slots, event=event)


@app.route('/event_participants/<int:event_id>', methods=["GET", "POST"])
@login_required
def event_participants(event_id):
    """ Event participants view """
    if request.method == 'GET':
        eid = event_id
        slots = None
        women = []
        men = []
        inw = []
        inm = []
        mailinw = []
        mailoutw = []
        mailinm = []
        mailoutm = []

        try:
            event = Events.query.filter(Events.id == eid).first()
            slots = TimeSlots.query.filter(TimeSlots.event_id == eid)
            if slots != None:
                for slot in slots:
                    women = Participants.query.order_by(
                        (Participants.creation_timestamp)).filter(
                            Participants.event_id == eid,
                            Participants.available_slot == slot.id,
                            Participants.gender == '1').all()
                    men = Participants.query.order_by(
                        (Participants.creation_timestamp)).filter(
                            Participants.event_id == eid,
                            Participants.available_slot == slot.id,
                            Participants.gender == '0').all()
                    women.append(women)
                    men.append(men)
        except Exception as e:
            print(e)
            return render_template('error.html')

    for wslot in women:
        inmail = ""
        outmail = ""
        wcount = 0
        for women in wslot:
            if women.confirmed == 1 and wcount < 12:
                wcount = wcount + 1
                inw.append(women.email)
                inmail = inmail + women.email + "; "
            else:
                outmail = outmail + women.email + "; "

        mailinw.append(inmail)
        mailoutw.append(outmail)

    for mslot in men:
        inmail = ""
        outmail = ""
        mcount = 0
        for men in mslot:
            if men.confirmed == 1 and mcount < 12:
                mcount = mcount + 1
                inm.append(men.email)
                inmail = inmail + men.email + "; "
            else:
                outmail = outmail + men.email + "; "
        mailinm.append(inmail)
        mailoutm.append(outmail)

    return render_template(
        'event_participants.html',
        event=event,
        slots=slots,
        women=women,
        men=men,
        inw=inw,
        inm=inm,
        mailinw=mailinw,
        mailinm=mailinm,
        mailoutw=mailoutw,
        mailoutm=mailoutm)


@app.route('/create_event', methods=["GET", "POST"])
@login_required
def create_event():
    """ Event create view """
    form = CreateEventForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            format_string = '%Y-%m-%dT%H:%M'
            name = str(request.form['name'])
            year = int(request.form['year'])
            semester = int(request.form['semester'])
            specialslot = int(request.form['specialslot'])
            specialslotname = str(request.form['specialslotname'])
            specialslotdescription = str(
                request.form['specialslotdescription'])
            timestamp = datetime.now()
            opensignuptimestamp = datetime.strptime(
                str(request.form['opensignuptimestamp']), format_string)
            closesignuptimestamp = datetime.strptime(
                str(request.form['closesignuptimestamp']), format_string)
            place = str(request.form['place'])
            participationfee = str(request.form['participationfee'])
            signup_open = 0
            active = 0

        except Exception as e:
            print(e)
            return render_template(
                'error.html', message=str(request.form['opensignuptimestamp']))

        try:
            event = Events(name, year, specialslot, specialslotname,
                           specialslotdescription, place, semester, timestamp,
                           signup_open, active, participationfee,
                           opensignuptimestamp, closesignuptimestamp)
            db.session.add(event)
            db.session.commit()
        except Exception as e:
            print(e)
            return render_template('error.html')
        return redirect(url_for('admin'))
    return render_template('create_event.html', form=form)


@app.route('/create_timeslot/<int:event_id>', methods=["GET", "POST"])
@login_required
def create_timeslot(event_id):
    """ Timeslot create view """
    form = CreateTimeSlotForm(request.form)
    eventid = event_id
    if request.method == 'POST' and form.validate():
        try:
            date = str(request.form['date'])
            starttime = str(request.form['starttime'])
            endtime = str(request.form['endtime'])
            nrcouples = int(request.form['nrcouples'])
            agerange = int(request.form['agerange'])
            specialslot = int(request.form['specialslot'])
            slot = TimeSlots(eventid, date, starttime, endtime, nrcouples,
                             agerange, specialslot)
            db.session.add(slot)
            db.session.commit()

        except Exception as e:
            print(e)
            return render_template('error.html')

        return redirect(url_for('event_view', event_id=eventid))
    return render_template('create_timeslot.html', eid=eventid, form=form)


@app.route('/timeslot_view/<int:timeslot_id>', methods=["GET", "POST"])
@login_required
def timeslot_view(timeslot_id):
    """ Timeslot view """
    if request.method == 'GET':

        slotid = timeslot_id

        [w_in, w_out] = get_list_women_of_slot(db.session, timeslot_id)
        [m_in, m_out] = get_list_men_of_slot(db.session, timeslot_id)

        try:
            slot = TimeSlots.query.filter(TimeSlots.id == slotid).first()
            women = Participants.query.order_by(
                (Participants.creation_timestamp)).filter(
                    Participants.available_slot == slotid,
                    Participants.gender == '1').all()
            men = Participants.query.order_by(
                (Participants.creation_timestamp)).filter(
                    Participants.available_slot == slotid,
                    Participants.gender == '0').all()
            event = Events.query.filter(Events.id == slot.event_id).first()
        except Exception as e:
            print(e)
            return render_template('error.html')

        w_in_mail = get_string_mails_of_list(db.session, slot, w_in)
        w_out_mail = get_string_mails_of_list(db.session, slot, w_out)
        m_in_mail = get_string_mails_of_list(db.session, slot, m_in)
        m_out_mail = get_string_mails_of_list(db.session, slot, m_out)

        return render_template(
            'timeslot_view.html',
            event=event,
            slot=slot,
            women=women,
            men=men,
            inw=w_in,
            inm=m_in,
            mailinw=w_in_mail,
            mailinm=m_in_mail,
            mailoutw=w_out_mail,
            mailoutm=m_out_mail)


@app.route('/timeslot_view_ongoing/<int:timeslot_id>', methods=["GET", "POST"])
@login_required
def timeslot_view_ongoing(timeslot_id):
    """ View to assign date numbers to participants """
    form = DateNrChangeForm(request.form)
    csv = ''

    if request.method == 'POST' and form.validate():
        try:
            participant_id = int(request.form['participant_id'])
            datenr = int(request.form['datenr'])
            if not change_datenr(db.session, participant_id, datenr):
                return render_template('error.html', message='Datenr. konnte nicht geändert werden')

        except Exception as e:
            print(e)
            return render_template('error.html')

    # "GET":
    try:
        slot = TimeSlots.query.filter(TimeSlots.id == timeslot_id).first()
        women = Participants.query.order_by(
            (Participants.creation_timestamp)).filter(
                Participants.available_slot == timeslot_id,
                Participants.gender == '1', Participants.present == '1').all()
        men = Participants.query.order_by(
            (Participants.creation_timestamp)).filter(
                Participants.available_slot == timeslot_id,
                Participants.gender == '0', Participants.present == '1').all()
        event = Events.query.filter(Events.id == slot.event_id).first()
    except Exception as e:
        print(e)
        return render_template('error.html')
    form.datenr.data = ''
    return render_template(
        'timeslot_view_ongoing.html',
        event=event,
        slot=slot,
        women=women,
        men=men,
        form=form,
        csv=csv)


@app.route('/change_signup/<int:event_id>/<int:open>', methods=["GET", "POST"])
@login_required
def change_signup(event_id, open):
    """ Action to open/close the signup """
    try:
        changed = event_change_signup_status(db.session, event_id, open)
    except Exception as e:
        print(e)
        return render_template('error.html')
    if changed:
        return redirect(url_for('admin'))
    return render_template('error.html')


@app.route(
    '/activate_event/<int:event_id>/<int:active>', methods=["GET", "POST"])
@login_required
def activate_event(event_id, active):
    """ Action to activate / deactivate an event.
    Activating an event will show the info on the front page.
    """
    try:
        activated = event_change_active_status(db.session, event_id, active)
    except Exception as e:
        print(e)
        return render_template('error.html')
    if activated:
        return redirect(url_for('admin'))
    return render_template('error.html')


@app.route(
    '/register_participant/<int:event_id>/<int:participant_id>',
    methods=["GET", "POST"])
@login_required
def register_participant(event_id, participant_id):
    """ Action to confirm / cancel a participant
    """

    try:
        registered = event_change_register_status(db.session, participant_id)
    except Exception as e:
        print(e)
        return render_template('error.html')
    if registered:
        return redirect(url_for('event_participants', event_id=event_id))
    return render_template('error.html')


@app.route(
    '/change_participant_on_timeslot/<int:slot_id>/<int:participant_id>/<string:action>',
    methods=["GET", "POST"])
@login_required
def change_participant_on_timeslot(slot_id, participant_id, action):
    """ Action to confirm attendance and payment """
    try:
        if action == 'present':
            changed = change_present(db.session, participant_id)
        elif action == 'payed':
            changed = change_payed(db.session, participant_id)
    except Exception as e:
        print(e)
        return render_template('error.html')
    if changed:
        return redirect(url_for('timeslot_view', timeslot_id=slot_id))
    return render_template(
        'error.html',
        message='changing ' + action +
        ' did not work. Maybe a participant wanted to pay before being present on event.'
    )


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """ Main signup page """
    form = SignupForm(request.form)
    try:
        event = Events.query.filter(Events.active == '1').first()
        if event != None:
            eventid = event.id
            timeslots = TimeSlots.query.filter(
                TimeSlots.event_id == eventid).all()
            if timeslots != None:
                age_strings = []
                age_strings.append('< 22'.ljust(6))
                age_strings.append('22-25'.ljust(6))
                age_strings.append('> 25'.ljust(6))
                age_strings.append('alle'.ljust(6))
                ids_nonspecial = []
                ids_special = []
                strings_non_special = []
                strings_special = []
                for s in timeslots:
                    if s.special_slot == 1:
                        ids_special.append(int(s.id))
                        women = Participants.query.filter(
                            Participants.available_slot == s.id,
                            Participants.confirmed == '1',
                            Participants.gender == '1').count()
                        men = Participants.query.filter(
                            Participants.available_slot == s.id,
                            Participants.confirmed == '1',
                            Participants.gender == '0').count()
                        stri = '&nbsp &nbsp &nbsp'
                        stri = stri + \
                            s.date.strftime("%a %d. %b %y") + \
                            '&nbsp &nbsp &nbsp'
                        stri = str(stri).ljust(50, ' ' [0:1]) + str(
                            s.start_time)[:-3] + ' - ' + str(s.end_time)[:-3]
                        stri = stri + '&nbsp &nbsp &nbsp'
                        stri = stri + 'Altersgruppe: &nbsp' + \
                            age_strings[s.age_range]
                        stri = stri + '&nbsp &nbsp &nbsp Anmeldungsstand: &nbsp &nbsp  M: ' + \
                            str(men) + '/' + str(s.nr_couples)
                        stri = stri + '&nbsp &nbsp W: ' + \
                            str(women) + '/' + str(s.nr_couples)
                        strings_special.append(stri)
                    elif s.special_slot == 0:
                        ids_nonspecial.append(int(s.id))
                        women = Participants.query.filter(
                            Participants.available_slot == s.id,
                            Participants.confirmed == '1',
                            Participants.gender == '1').count()
                        men = Participants.query.filter(
                            Participants.available_slot == s.id,
                            Participants.confirmed == '1',
                            Participants.gender == '0').count()
                        stri = '&nbsp &nbsp &nbsp'
                        stri = stri + \
                            s.date.strftime("%a %d. %b %y") + \
                            '&nbsp &nbsp &nbsp'
                        stri = str(stri).ljust(50, ' ' [0:1]) + str(
                            s.start_time)[:-3] + ' - ' + str(s.end_time)[:-3]
                        stri = stri + '&nbsp &nbsp &nbsp'
                        stri = stri + 'Altersgruppe: &nbsp' + \
                            age_strings[s.age_range]
                        stri = stri + '&nbsp &nbsp &nbsp Anmeldungsstand: &nbsp &nbsp  M: ' + \
                            str(men) + '/' + str(s.nr_couples)
                        stri = stri + '&nbsp &nbsp W: ' + \
                            str(women) + '/' + str(s.nr_couples)
                        strings_non_special.append(stri)

                form.availableslots.choices = [
                    (ids_nonspecial[i], strings_non_special[i])
                    for i in range(0, len(ids_nonspecial))
                ]
                form.availablespecialslots.choices = [
                    (ids_special[i], strings_special[i])
                    for i in range(0, len(ids_special))
                ]

    except Exception as e:
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
            if event.special_slots == 1:
                availablespecialslots = request.form.getlist(
                    'availablespecialslots')
            availableslots = request.form.getlist('availableslots')
            confirmed = 1
            present = 0
            payed = 0

            slots = 0
            if availableslots:
                slots = int(availableslots[0])
            elif availablespecialslots:
                slots = int(availablespecialslots[0])
            else:
                message = 'Du hast kein passendes Datum ausgewählt! Bitte geh zurück und wähle ein dir passendes Datum aus.'
                return render_template('error.html', message=message)

            bday = datetime.strptime(birthday, '%d.%m.%Y')
            count = Participants.query.filter(
                Participants.email == email,
                Participants.event_id == eventid).count()
            chosen_timeslot = TimeSlots.query.filter(
                TimeSlots.id == int(slots)).first()
            chosen_datetime = str(
                chosen_timeslot.date.strftime("%a %d. %b %y")) + '  ' + str(
                    chosen_timeslot.start_time)

            if count == 0:
                new_participant = Participants(
                    timestamp,
                    eventid,
                    name,
                    prename,
                    email,
                    mobile,
                    address,
                    bday,
                    gender,
                    course=studycourse,
                    semester=studysemester,
                    perfDate=perfectdate,
                    fruit=fruit,
                    aSlot=slots,
                    confirmed=confirmed,
                    present=present,
                    payed=payed)
                db.session.add(new_participant)
                db.session.commit()

                # The participant signed up successfully
                # Emit signal and show success page
                SIGNAL_NEW_SIGNUP.send('signup view', participant=new_participant)
            else:
                message = 'Die E-Mail Adresse ' + email + \
                    ' wurde bereits für das Speeddating angewendet. Bitte versuchen Sie es erneut mit einer neuen E-Mail Adresse.'
                return render_template('error.html', message=message)

        except Exception as e:
            print('Exception of type {} occurred'.format(type(e)))
            return render_template('error.html')

        return render_template(
            'success.html',
            name=(prename + ' ' + name),
            mail=email,
            datetime=chosen_datetime)

    return render_template('signup.html', form=form, event=event)


@app.route('/manual_signup', methods=["GET", "POST"])
@login_required
def manual_signup():
    """ Admin signup page, allows signup outside of registration period """
    form = SignupForm(request.form)
    try:
        event = Events.query.filter(Events.active == '1').first()
        if event != None:
            eventid = event.id
            timeslots = TimeSlots.query.filter(
                TimeSlots.event_id == eventid).all()
            if timeslots != None:
                age_strings = []
                age_strings.append('< 22'.ljust(6))
                age_strings.append('22-25'.ljust(6))
                age_strings.append('> 25'.ljust(6))

                ids = []
                strings = []
                for s in timeslots:
                    ids.append(int(s.id))
                    women = Participants.query.filter(
                        Participants.available_slot == s.id,
                        Participants.confirmed == '1',
                        Participants.gender == '1').count()
                    men = Participants.query.filter(
                        Participants.available_slot == s.id,
                        Participants.confirmed == '1',
                        Participants.gender == '0').count()
                    stri = '&nbsp &nbsp '
                    stri = stri + \
                        s.date.strftime("%a %d. %B %Y") + '&nbsp &nbsp '
                    stri = str(stri).ljust(50, ' ' [0:1]) + str(
                        s.start_time)[:-3] + ' - ' + str(s.end_time)[:-3]
                    stri = stri + '&nbsp &nbsp '
                    stri = stri + 'Altersgruppe: &nbsp' + \
                        age_strings[s.age_range]
                    stri = stri + \
                        '&nbsp &nbsp # angemeldete Personen: &nbsp &nbsp  M: ' + \
                        str(men)
                    stri = stri + '&nbsp &nbsp W: ' + str(women)
                    strings.append(stri)

                form.availableslots.choices = [
                    (ids[i], strings[i]) for i in range(0, len(timeslots))
                ]

    except Exception as e:
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

            bday = datetime.strptime(birthday, '%d.%m.%Y')

            count = Participants.query.filter(
                Participants.email == email,
                Participants.event_id == eventid).count()

            if count == 0:
                new_participant = Participants(
                    timestamp,
                    eventid,
                    name,
                    prename,
                    email,
                    mobile,
                    address,
                    bday,
                    gender,
                    course=studycourse,
                    semester=studysemester,
                    perfDate=perfectdate,
                    fruit=fruit,
                    aSlot=availableslots,
                    confirmed=confirmed,
                    present=present,
                    payed=payed)
                db.session.add(new_participant)
                db.session.commit()
            else:
                message = 'Die E-Mail Adresse ' + email + \
                    ' wurde bereits für das Speeddating angewendet.\
                    Bitte versuchen Sie es erneut mit einer neuen E-Mail Adresse.'
                return render_template('error.html', message=message)

        except Exception as exception:
            print(exception)
            return render_template('error.html')

        return render_template('success.html')
    return render_template('manual_signup.html', form=form, event=event)


@app.route('/export_slot/<int:timeslot_id>', methods=["GET", "POST"])
@login_required
def export_slot(timeslot_id):
    """ Export participants of timeslot as CSV suitable for SpeedMatchTool"""
    try:
        slot = TimeSlots.query.filter(TimeSlots.id == timeslot_id).first()
        women = Participants.query.order_by(
            (Participants.creation_timestamp)).filter(
                Participants.available_slot == timeslot_id,
                Participants.gender == '1', Participants.present == '1').all()
        men = Participants.query.order_by(
            (Participants.creation_timestamp)).filter(
                Participants.available_slot == timeslot_id,
                Participants.gender == '0', Participants.present == '1').all()
        exported = export(women, men, slot)

    except Exception as e:
        print(e)
        return render_template('error.html')

    if exported != '':
        return render_template('csv.html', slot=slot, exported=exported)
    return render_template('error.html')

@app.route('/confirm/<string:confirm_token>')
def confirm_participation(confirm_token):
    """ Use confirm_token to confirm participation """
    if _confirm_participation(confirm_token):
        return render_template('confirm_success.html')
    abort(404)

@app.route('/cancel/<string:cancel_token>')
def cancel_participation(cancel_token):
    """ Use cancel_token to cancel participation """
    if _cancel_participation(cancel_token):
        return render_template('cancel_success.html')
    abort(404)
