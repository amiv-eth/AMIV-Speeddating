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


    
def event_change_register_status(session, p_id, register):
    try:
        participant = session.query(Participants).filter_by(ID = p_id).first()
        if participant.Confirmed == 0:
            participant.Confirmed = 1
        else:
            participant.Confirmed = 0
        session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def change_present(session, slot_id, participant_id):
    try:
        participant = session.query(Participants).filter_by(ID = participant_id).first()
        
        if participant.Present == 0:
            participant.Present = int(1)
        else:
            participant.Present = int(0)

        session.commit()
        return True
    except Exception as e:
        print(e)
        return False


def change_payed(session, slot_id, participant_id):
    try:
        participant = session.query(Participants).filter_by(ID = participant_id).first()

        if participant.Present == 1:
            if participant.Payed == 0:
                participant.Payed = int(1)
            else:
                participant.Payed = int(0)
        else:
            return False

        session.commit()
        return True
    except Exception as e:
        print(e)
        return False


def change_datenr(session, participant_id, datenr):
    try:
        participant = session.query(Participants).filter_by(ID = participant_id).first()
      
        participant.DateNr = int(datenr)

        session.commit()
        return True
    except Exception as e:
        print(e)
        return False
