from apps.models import Participants, TimeSlots, Events

def change_signup_status(db, event_id, open):
    try:
        event = db.session.query(Events).filter_by(ID = event_id).first()
        event.SignupOpen= int(open)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def activate_event_status(db, event_id, active):
    try:
        event = db.session.query(Events).filter_by(ID = event_id).first()
        event.Active= int(active)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False


