from app.models import Participants, TimeSlots, Events

def event_change_signup_status(session, event_id, open):
    try:
        event = session.query(Events).filter_by(ID = event_id).first()
        
        if event.Active == 1:
            if open == 1:
                event.SignupOpen= int(open)
            else:
                event.SignupOpen= int(open)
        else:
            if open == 0:
                event.SignupOpen= int(open)
        session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def event_change_active_status(session, event_id, active):
    try:
        nr_active_events = session.query(Events).filter(Events.Active == active).count()

        if active == 1:
            if nr_active_events > 0:
                events = session.query(Events).all()
                for e in events:
                    event_change_signup_status(session, e.ID, 0)
                    e.Active = 0
                    
            event = session.query(Events).filter(Events.ID == event_id).first()
            event.Active = int(active)

        if active == 0:
            event_change_signup_status(session, event_id, 0)
            event = session.query(Events).filter(Events.ID == event_id).first()
            event.Active = int(active)

        session.commit()
        return True

    except Exception as e:
        print(e)
        return False


