"""
Contains admin helper functions
"""
import csv
import io
from app.models import Participants, Events
from app import db


def event_change_active_status(event_id, active):
    """ Set an event to active / inactive """
    nr_active_events = Events.query.filter_by(active=active).count()

    # Set event to active
    if active == 1:
        # Assert that there is at most one active event
        if nr_active_events > 0:
            events = Events.query.all()
            for event in events:
                event.active = False

        event = Events.query.get(event_id)
        if event is None:
            return False

        event.active = True

    # Deactivate event
    if active == 0:
        event = Events.query.get(event_id)
        if event is None:
            return False

        event.active = False

    db.session.commit()
    return True


def event_change_register_status(p_id):
    """ Confirm / unconfirm a participant's registration """
    try:
        participant = Participants.query.get(p_id)
        if participant is None:
            return False

        if not participant.confirmed:
            participant.confirmed = True
        else:
            participant.confirmed = False

        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False


def change_present(participant_id):
    """ Mark a participant as present / absent """
    try:
        participant = Participants.get(participant_id)
        if participant is None:
            return False

        if not participant.present:
            participant.present = True
        else:
            participant.present = False

        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False


def change_paid(participant_id):
    """ Set a participant's payment status """
    try:
        participant = Participants.query.get(participant_id)
        if participant is None:
            return False

        if participant.present:
            if not participant.paid:
                participant.paid = True
            else:
                participant.paid = False
        else:
            return False

        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False


def change_datenr(participant_id, datenr):
    """ Change a participant's date number """
    participant = Participants.query.get(participant_id)
    if participant is None:
        return False

    participant.date_nr = datenr
    db.session.commit()
    return True


def export(women, men, slot):
    """ Export a slot's participant list as CSV """
    try:
        output = io.StringIO()
        res = csv.writer(output, delimiter=',')
        for w in women:
            res.writerow([str(w.date_nr)] + ['f'] + [w.prename] + [w.name] +
                         [str(w.get_age())] + [w.mobile_nr] + [w.email])
        for m in men:
            res.writerow([str(m.date_nr)] + ['m'] + [m.prename] + [m.name] +
                         [str(m.get_age())] + [m.mobile_nr] + [m.email])

        result = output.getvalue()
        output.close()
        return str(result)
    except Exception as e:
        print(e)
        return ''


def registration_opened(event):
    """ Hook for after an Event's signup_open is automatically set to True """
    print('Signup for event {} has been opened'.format(event))


def registration_closed(event):
    """ Hook for after an Event's signup_open is automatically set to False """
    print('Signup for event {} has been closed'.format(event))
