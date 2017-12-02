from app.models import Participants, TimeSlots, Events
import csv
import datetime
from datetime import date
import io


def event_change_signup_status(session, event_id, open):
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


def event_change_register_status(session, p_id, register):
    try:
        participant = session.query(Participants).filter_by(id=p_id).first()
        if participant.confirmed == 0:
            participant.confirmed = 1
        else:
            participant.confirmed = 0
        session.commit()
        return True
    except Exception as e:
        print(e)
        return False


def change_present(session, slot_id, participant_id):
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


def change_payed(session, slot_id, participant_id):
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
    try:
        output = io.StringIO()
        res = csv.writer(output, delimiter=',')
        for w in women:
            res.writerow([str(w.date_nr)] + ['f'] + [w.prename] + [w.name] +
                         [str(get_age(w.birthday))] + [w.mobile_nr] + [w.email])
        for m in men:
            res.writerow([str(m.date_nr)] + ['m'] + [m.prename] + [m.name] +
                         [str(get_age(m.birthday))] + [m.mobile_nr] + [m.email])

        result = output.getvalue()
        output.close()
        return str(result)
    except Exception as e:
        print(e)
        return ''


def get_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) <
                                     (born.month, born.day))
