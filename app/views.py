"""
Contains all views, i.e. anything that is routed to a url

"""

from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from app.models import Events, TimeSlots, Participants, AdminUser, Gender, Semester
from app.forms import LoginForm, CreateEventForm, CreateTimeSlotForm, SignupForm, DateNrChangeForm, LikeForm, SendMatchesForm
from app.help_queries import participants_in_slot, get_string_of_date_list
from app.admin import export, change_datenr, change_paid, change_present, event_change_register_status, event_change_active_status
from app import app, db, login_manager, bcrypt, mail
from datetime import datetime
from flask_mail import Message
from app.signals import SIGNAL_NEW_SIGNUP
from app.participants import confirm_participation as _confirm_participation, cancel_participation as _cancel_participation
from app.signup import get_slots_choices
from app.matcher import find_matches, inform_matches


@app.route('/')
@app.route('/index')
def index():
    """ Index """
    try:
        # Only one event is shown at a time
        event = Events.query.filter(Events.active).first()
        dates = None
        if event is not None:
            timeslots = TimeSlots.query.filter(TimeSlots.event_id == event.id).all()
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
    """ Catchall for unauthorized requests, redirect to login """
    return redirect(url_for('login'))


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
    """ Show timeslots of event """
    if request.method == 'GET':
        event = Events.query.get_or_404(event_id)
        slots = TimeSlots.query.filter(TimeSlots.event_id == event_id)
        nr_women_total = []
        nr_women_confirmed = []
        nr_men_total = []
        nr_men_confirmed = []
        if slots != None:
            for slot in slots:
                nr_women_total.append(slot.participants.filter_by(gender=Gender.FEMALE).count())
                nr_women_confirmed.append(slot.participants.filter_by(confirmed=True, gender=Gender.FEMALE).count())
                nr_men_total.append(slot.participants.filter_by(gender=Gender.MALE).count())
                nr_men_confirmed.append(slot.participants.filter_by(confirmed=True, gender=Gender.MALE).count())
        return render_template('event_view.html', slots=slots, event=event, nr_women_total=nr_women_total, nr_women_confirmed=nr_women_confirmed, nr_men_total=nr_men_total, nr_men_confirmed=nr_men_confirmed)


@app.route('/event_participants/<int:event_id>', methods=["GET", "POST"])
@login_required
def event_participants(event_id):
    """ Shows all participants in all timeslots of an event, confirmed or not """
    if request.method == 'GET':
        women = []
        men = []
        inw = []
        inm = []
        mailinw = []
        mailoutw = []
        mailinm = []
        mailoutm = []

        event = Events.query.get_or_404(event_id)

        slots = TimeSlots.query.filter(TimeSlots.event_id == event_id)
        if slots is not None:
            for slot in slots:
                women.append(slot.get_participants(gender=Gender.FEMALE))
                men.append(slot.get_participants(gender=Gender.MALE))

                inw.extend(p.email for p in slot.get_participants(on_waiting_list=False, gender=Gender.FEMALE))
                inm.extend(p.email for p in slot.get_participants(on_waiting_list=False, gender=Gender.MALE))

                # Create email strings
                mailinw.append('; '.join(p.email for p in slot.get_participants(on_waiting_list=False, gender=Gender.FEMALE)))
                mailoutw.append('; '.join(p.email for p in slot.get_participants(on_waiting_list=True, gender=Gender.FEMALE)))
                mailinm.append('; '.join(p.email for p in slot.get_participants(on_waiting_list=False, gender=Gender.MALE)))
                mailoutm.append('; '.join(p.email for p in slot.get_participants(on_waiting_list=True, gender=Gender.MALE)))

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
            semester = Semester(int(request.form['semester']))
            specialslot = int(request.form['special_slots'])
            specialslotname = str(request.form['special_slots_name'])
            specialslotdescription = str(
                request.form['special_slots_description'])
            timestamp = datetime.now()
            opensignuptimestamp = datetime.strptime(
                str(request.form['open_signup_timestamp']), format_string)
            closesignuptimestamp = datetime.strptime(
                str(request.form['close_signup_timestamp']), format_string)
            place = str(request.form['place'])
            participationfee = str(request.form['participation_fee'])
            signup_open = False
            active = False

        except Exception as e:
            print(e)
            return render_template(
                'error.html', message=str(request.form['opensignuptimestamp']))

        try:
            event = Events(name=name, year=year, special_slots=specialslot, special_slots_name=specialslotname,
                           special_slots_description=specialslotdescription, place=place, semester=semester,
                           creation_timestamp=timestamp, signup_open=signup_open, active=active,
                           participation_fee=participationfee, open_signup_timestamp=opensignuptimestamp,
                           close_signup_timestamp=closesignuptimestamp)
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
    event = Events.query.get_or_404(event_id)
    if request.method == 'POST' and form.validate():
        try:
            d = str(request.form['date'])
            date = datetime.strptime(d, '%d.%m.%Y')
            starttime = str(request.form['start_time'])
            endtime = str(request.form['end_time'])
            nrcouples = int(request.form['nr_couples'])
            agerange = int(request.form['age_range'])
            specialslot = int(request.form['special_slot'])
            slot = TimeSlots(event_id=event.id, date=date, start_time=starttime, end_time=endtime,
                             nr_couples=nrcouples, age_range=agerange, special_slot=specialslot)
            db.session.add(slot)
            db.session.commit()

        except Exception as e:
            print(e)
            return render_template('error.html')

        return redirect(url_for('event_view', event_id=event.id))
    return render_template('create_timeslot.html', event=event, form=form)


@app.route('/timeslot_view/<int:timeslot_id>', methods=["GET", "POST"])
@login_required
def timeslot_view(timeslot_id):
    """ Timeslot view """
    if request.method == 'GET':
        slot = TimeSlots.query.get_or_404(timeslot_id)

        [w_in, w_out] = participants_in_slot(slot, gender=Gender.FEMALE, confirmed=1)
        [m_in, m_out] = participants_in_slot(slot, gender=Gender.MALE, confirmed=1)

        try:
            women = slot.participants.filter_by(gender=Gender.FEMALE).order_by(Participants.creation_timestamp).all()
            men = slot.participants.filter_by(gender=Gender.MALE).order_by(Participants.creation_timestamp).all()
            event = Events.query.filter(Events.id == slot.event_id).first()
        except Exception as e:
            print(e)
            return render_template('error.html')

        # Create semicolon-separated list of email addresses
        w_in_mail = '; '.join([w.email for w in w_in])
        w_out_mail = '; '.join([w.email for w in w_out])
        m_in_mail = '; '.join([m.email for m in m_in])
        m_out_mail = '; '.join([m.email for m in m_out])

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

    if request.method == 'POST' and form.validate():
        try:
            participant_id = int(request.form['participant_id'])
            datenr = int(request.form['datenr'])
            if not change_datenr(participant_id, datenr):
                return render_template('error.html', message='Datenr. konnte nicht geändert werden')
        except Exception as e:
            print(e)
            return render_template('error.html')

    # "GET":
    try:
        form.datenr.data = ""
        slot = TimeSlots.query.get_or_404(timeslot_id)
        women = slot.get_participants(gender=Gender.FEMALE, present=True)
        men = slot.get_participants(gender=Gender.MALE, present=True)
        event = Events.query.get(slot.event_id)
        if event is None:
            return render_template('error.html', message='Timeslot has invalid event id')
    except Exception as e:
            print(e)
            return render_template('error.html')

    return render_template(
        'timeslot_view_ongoing.html',
        event=event,
        slot=slot,
        women=women,
        men=men,
        form=form)


@app.route('/activate_event/<int:event_id>/<int:active>', methods=["GET", "POST"])
@login_required
def activate_event(event_id, active):
    """ Action to activate / deactivate an event.
    Activating an event will show the info on the front page.
    """
    if not event_change_active_status(event_id, active):
        return render_template('error.html', message='Unable to change event status')
    return redirect(url_for('admin'))


@app.route(
    '/register_participant/<int:event_id>/<int:participant_id>',
    methods=["GET", "POST"])
@login_required
def register_participant(event_id, participant_id):
    """ Action to confirm / cancel a participant """
    try:
        registered = event_change_register_status(participant_id)
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
            changed = change_present(participant_id)
        elif action == 'paid':
            changed = change_paid(participant_id)
        elif action == 'register':
            changed = event_change_register_status(participant_id)
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
        event = Events.query.filter(Events.active).first()
        if event != None:
            eventid = event.id
            timeslots = TimeSlots.query.filter(
                TimeSlots.event_id == eventid).all()
            if timeslots != None:
                [available_slots_choices, available_special_slots_choices] = get_slots_choices(
                    timeslots)

                form.availableslots.choices = available_slots_choices
                form.availablespecialslots.choices = available_special_slots_choices

    except Exception as e:
        print(e)
        return render_template('error.html')

    if request.method == 'POST' and form.validate():
        try:
            timestamp = datetime.now()
            name = str(request.form['name'])
            prename = str(request.form['prename'])
            gender = Gender(int(request.form['gender']))
            email = str(request.form['email'])
            mobile = str(request.form['mobile_nr'])
            address = str(request.form['address'])
            birthday = str(request.form['birthday'])
            studycourse = str(request.form['study_course'])
            studysemester = int(request.form['study_semester'])
            perfectdate = str(request.form['perfect_date'])
            fruit = str(request.form['fruit'])
            availablespecialslots = None
            if event.special_slots:
                availablespecialslots = request.form.getlist(
                    'availablespecialslots')
            availableslots = request.form.getlist('availableslots')
            confirmed = False
            present = False
            paid = False
            slots = 0
            if availableslots:
                slots = int(availableslots[0])
            elif availablespecialslots:
                slots = int(availablespecialslots[0])
            else:
                message = 'Du hast kein passendes Datum ausgewählt!\
                Bitte geh zurück und wähle ein dir passendes Datum aus.'
                return render_template('error.html', message=message)
            bday = datetime.strptime(birthday, '%d.%m.%Y')
            chosen_timeslot = TimeSlots.query.filter(
                TimeSlots.id == int(slots)).first()
            chosen_datetime = str(
                chosen_timeslot.date.strftime("%a %d. %b %y")) + '  ' + str(
                    chosen_timeslot.start_time)
            try:
                new_participant = Participants(
                    creation_timestamp=timestamp,
                    event_id=eventid,
                    name=name,
                    prename=prename,
                    email=email,
                    mobile_nr=mobile,
                    address=address,
                    birthday=bday,
                    gender=gender,
                    study_course=studycourse,
                    study_semester=studysemester,
                    perfect_date=perfectdate,
                    fruit=fruit,
                    slot=slots,
                    confirmed=confirmed,
                    present=present,
                    paid=paid)
                db.session.add(new_participant)
                db.session.commit()
                # The participant signed up successfully
                # Emit signal and show success page
                SIGNAL_NEW_SIGNUP.send(
                    'signup view', participant=new_participant)
            except Participants.AlreadySignedUpException:
                message = 'Die E-Mail Adresse ' + email + \
                    ' wurde bereits für das Speeddating angewendet.\
                    Bitte versuchen Sie es erneut mit einer neuen E-Mail Adresse.'
                return render_template('error.html', message=message)

        except Exception as e:
            print('Exception of type {} occurred: {}'.format(type(e), str(e)))
            return render_template('error.html')

        return render_template(
            'success.html',
            name=('{} {}'.format(prename, name)),
            mail=email,
            datetime=chosen_datetime)

    return render_template('signup.html', form=form, event=event)


@app.route('/manual_signup', methods=["GET", "POST"])
@login_required
def manual_signup():
    """ Admin signup page, allows signup outside of registration period """
    form = SignupForm(request.form)
    try:
        event = Events.query.filter(Events.active).first()
        if event != None:
            eventid = event.id
            timeslots = TimeSlots.query.filter(
                TimeSlots.event_id == eventid).all()
            if timeslots != None:
                [available_slots_choices, available_special_slots_choices] = get_slots_choices(
                    timeslots)

                form.availableslots.choices = available_slots_choices
                form.availablespecialslots.choices = available_special_slots_choices

    except Exception as e:
        print(e)
        return render_template('error.html')

    if request.method == 'POST' and form.validate():
        try:
            timestamp = datetime.now()
            name = str(request.form['name'])
            prename = str(request.form['prename'])
            gender = Gender(int(request.form['gender']))
            email = str(request.form['email'])
            mobile = str(request.form['mobilenr'])
            address = str(request.form['address'])
            birthday = str(request.form['birthday'])
            studycourse = str(request.form['studycourse'])
            studysemester = int(request.form['studysemester'])
            perfectdate = str(request.form['perfectdate'])
            fruit = str(request.form['fruit'])
            availablespecialslots = None
            if event.special_slots:
                availablespecialslots = request.form.getlist(
                    'availablespecialslots')
            availableslots = request.form.getlist('availableslots')
            confirmed = False
            present = False
            paid = False
            slots = 0
            if availableslots:
                slots = int(availableslots[0])
            elif availablespecialslots:
                slots = int(availablespecialslots[0])
            else:
                message = 'Du hast kein passendes Datum ausgewählt!\
                Bitte geh zurück und wähle ein dir passendes Datum aus.'
                return render_template('error.html', message=message)
            bday = datetime.strptime(birthday, '%d.%m.%Y')
            chosen_timeslot = TimeSlots.query.filter(
                TimeSlots.id == int(slots)).first()
            chosen_datetime = str(
                chosen_timeslot.date.strftime("%a %d. %b %y")) + '  ' + str(
                    chosen_timeslot.start_time)
            try:
                new_participant = Participants(
                    creation_timestamp=timestamp,
                    event_id=eventid,
                    name=name,
                    prename=prename,
                    email=email,
                    mobile_nr=mobile,
                    address=address,
                    birthday=bday,
                    gender=gender,
                    study_course=studycourse,
                    study_semester=studysemester,
                    perfect_date=perfectdate,
                    fruit=fruit,
                    slot=slots,
                    confirmed=confirmed,
                    present=present,
                    paid=paid)
                db.session.add(new_participant)
                db.session.commit()
                # The participant signed up successfully
                # Emit signal and show success page
                SIGNAL_NEW_SIGNUP.send(
                    'signup view', participant=new_participant)
            except Participants.AlreadySignedUpException:
                message = 'Die E-Mail Adresse ' + email + \
                    ' wurde bereits für das Speeddating angewendet.\
                    Bitte versuchen Sie es erneut mit einer neuen E-Mail Adresse.'
                return render_template('error.html', message=message)

        except Exception as e:
            print('Exception of type {} occurred: {}'.format(type(e), str(e)))
            return render_template('error.html')

        return render_template(
            'success.html',
            name=('{} {}'.format(prename, name)),
            mail=email,
            datetime=chosen_datetime)

    return render_template('manual_signup.html', form=form, event=event)

@app.route('/edit_participant/<int:timeslot_id>/<int:participant_id>', methods=["GET", "POST"])
@login_required
def edit_participant(timeslot_id, participant_id):
    """ Admin edit signed up participants, allows to do changes
        on an already signed up particpant """
    event = Events.query.filter(Events.active).first()
    slot = TimeSlots.query.get_or_404(timeslot_id)
    participant = Participants.query.get_or_404(participant_id)
    form = SignupForm(request.form, obj=participant)
    if event != None:
        eventid = event.id
        timeslots = TimeSlots.query.filter(
            TimeSlots.event_id == eventid).all()
        if timeslots != None:
            [available_slots_choices, available_special_slots_choices] = get_slots_choices(
                timeslots)
            form.availableslots.choices = available_slots_choices
            form.availablespecialslots.choices = available_special_slots_choices
    form.birthday.data = participant.birthday.strftime("%d.%m.%Y")
    if len(available_slots_choices) > 0:
        for i in range(0,len(available_slots_choices)):
            if participant.slot in available_slots_choices[i]:
                form.availableslots.data = [participant.slot]
    if len(available_special_slots_choices) > 0:
        for i in range(0,len(available_special_slots_choices)):
            if participant.slot in available_special_slots_choices[i]:
                form.availablespecialslots.data = [participant.slot]

    if request.method == 'POST' and form.validate():
        try:
            form.populate_obj(participant)
            gender = Gender(int(request.form['gender']))
            birthday = str(request.form['birthday'])
            participant.birthday = datetime.strptime(birthday, '%d.%m.%Y')
            participant.gender = gender
            availablespecialslots = None
            if event.special_slots:
                availablespecialslots = request.form.getlist(
                    'availablespecialslots')
            availableslots = request.form.getlist('availableslots')
            slots = 0
            if availableslots:
                slots = int(availableslots[0])
            elif availablespecialslots:
                slots = int(availablespecialslots[0])
            else:
                message = 'Du hast kein passendes Datum ausgewählt!\
                Bitte geh zurück und wähle ein dir passendes Datum aus.'
                return render_template('error.html', message=message)
            participant.slot = int(slots)
            db.session.commit()
        except Exception as e:
            print('Exception of type {} occurred: {}'.format(type(e), str(e)))
            return render_template('error.html')
        return redirect(request.referrer)
    return render_template('edit_participant.html', form=form, event=event, slot=slot, participant=participant)

@app.route('/edit_timeslot/<int:timeslot_id>', methods=["GET", "POST"])
@login_required
def edit_timeslot(timeslot_id):
    """ Admin edit timeslots, allows to do changes
        on an already created timeslot """
    event = Events.query.filter(Events.active).first()
    slot = TimeSlots.query.get_or_404(timeslot_id)
    form = CreateTimeSlotForm(request.form, obj=slot)
    form.special_slot.data = str(int(slot.special_slot))
    form.date.data = slot.date.strftime("%d.%m.%Y")
    if request.method == 'POST' and form.validate():
        try:
            form.populate_obj(slot)
            special_slot = int(request.form['special_slot'])
            date = str(request.form['date'])
            slot.special_slot = special_slot
            slot.date = datetime.strptime(date, '%d.%m.%Y')
            db.session.commit()
        except Exception as e:
            print('Exception of type {} occurred: {}'.format(type(e), str(e)))
            return render_template('error.html')
        return redirect(request.referrer)
    return render_template('edit_timeslot.html', form=form, slot=slot, event=event)


@app.route('/edit_event/<int:event_id>', methods=["GET", "POST"])
@login_required
def edit_event(event_id):
    """ Admin edit event, allows to do changes
        on an already created event """
    event = Events.query.get_or_404(event_id)
    form = CreateEventForm(request.form, obj=event)
    form.special_slots.data = str(int(event.special_slots))
    form.semester.data = str(event.semester.value)
    if request.method == 'POST' and form.validate():
        try:
            form.populate_obj(event)
            semester = Semester(int(request.form['semester']))
            event.semester = semester
            db.session.commit()
        except Exception as e:
            print('Exception of type {} occurred: {}'.format(type(e), str(e)))
            return render_template('error.html')
        return redirect(request.referrer)
    return render_template('edit_event.html', form=form, event=event)

@app.route('/export_slot/<int:timeslot_id>', methods=["GET", "POST"])
@login_required
def export_slot(timeslot_id):
    """ Export participants of timeslot as CSV suitable for SpeedMatchTool"""
    slot = TimeSlots.query.get_or_404(timeslot_id)

    # Fetch list of confirmed participants
    women = participants_in_slot(slot, Gender.FEMALE)[0]
    men = participants_in_slot(slot, Gender.MALE)[0]

    exported = export(women, men, slot)
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


@app.route('/edit_likes/<int:participant_id>', methods=['GET', 'POST'])
@login_required
def edit_likes(participant_id):
    """ Enter for each participant, which other participants they liked. """
    participant = Participants.query.get_or_404(participant_id)

    if request.method == 'GET':
        form = LikeForm(likes=participant.likes)
    else:
        form = LikeForm(request.form)
        if form.validate_on_submit():
            participant.likes = form.likes.data
            db.session.commit()
            return redirect(url_for('timeslot_view_ongoing', timeslot_id=participant.slot))

    return render_template('likes.html', form=form, participant_id=participant_id, email=participant.email)


@app.route('/matches/<int:timeslot_id>', methods=['GET', 'POST'])
@login_required
def matches(timeslot_id):
    """ Show the matches within a timeslot """
    slot = TimeSlots.query.filter(TimeSlots.id == timeslot_id).first()

    if request.method == 'POST':
        form = SendMatchesForm(request.form)
        if form.validate():
            inform_matches(find_matches(slot))
            return redirect(url_for('timeslot_view', timeslot_id=timeslot_id))

    matches = find_matches(slot)
    form = SendMatchesForm()
    return render_template('matches.html', matches=matches, form=form, timeslot_id=timeslot_id)
