"""
Contains admin helper functions
"""
import csv
import io
from app.models import Participants, Events


def event_change_signup_status(session, event_id, open):
    """ Open / close an event's signup window """
    try:
        event = Events.query.filter_by(id=event_id).first()
        if event.active == 1:
            if open == 1:
                event.signup_open = int(open)
            else:
                event.signup_open = int(open)
        else:
            if open == 0:
                event.signup_open = int(open)
        session.commit()
        return True
    except Exception as e:
        print(e)
        return False


def event_change_active_status(session, event_id, active):
    """ Set an event to active / inactive """
    try:
        nr_active_events = session.query(Events).filter(
            Events.active == active).count()

        if active == 1:
            if nr_active_events > 0:
                events = session.query(Events).all()
                for e in events:
                    event_change_signup_status(session, e.id, 0)
                    e.active = 0

            event = session.query(Events).filter(Events.id == event_id).first()
            event.active = int(active)

        if active == 0:
            event_change_signup_status(session, event_id, 0)
            event = session.query(Events).filter(Events.id == event_id).first()
            event.active = int(active)

        session.commit()
        return True

    except Exception as e:
        print(e)
        return False


def event_change_register_status(session, p_id):
    """ Confirm / unconfirm a participant's registration """
    try:
        participant = session.query(Participants).filter_by(id=p_id).first()
        if participant.confirmed is False:
            participant.confirmed = True
        else:
            participant.confirmed = False
        session.commit()
        return True
    except Exception as e:
        print(e)
        return False


def change_present(session, participant_id):
    """ Mark a participant as present / absent """
    try:
        participant = session.query(Participants).filter_by(
            id=participant_id).first()

        if participant.present == 0:
            participant.present = int(1)
        else:
            participant.present = int(0)

        session.commit()
        return True
    except Exception as e:
        print(e)
        return False


def change_payed(session, participant_id):
    """ Set a participant's payment status """
    try:
        participant = session.query(Participants).filter_by(
            id=participant_id).first()

        if participant.present == 1:
            if participant.payed == 0:
                participant.payed = int(1)
            else:
                participant.payed = int(0)
        else:
            return False

        session.commit()
        return True
    except Exception as e:
        print(e)
        return False


def change_datenr(session, participant_id, datenr):
    """ Change a participant's date number """
    try:
        participant = session.query(Participants).filter_by(
            id=participant_id).first()

        participant.date_nr = int(datenr)

        session.commit()
        return True
    except Exception as e:
        print(e)
        return False


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
