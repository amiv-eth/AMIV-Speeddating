from app.models import Participants, TimeSlots, Events

def event_change_signup_status(session, event_id, open):
    try:
        event = session.query(Events).filter_by(ID = event_id).first()
        event.SignupOpen= int(open)
        session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def event_change_active_status(session, event_id, active):
    try:
        event = session.query(Events).filter_by(ID = event_id).first()
        event.Active= int(active)
        session.commit()
        return True
    except Exception as e:
        print(e)
        return False


