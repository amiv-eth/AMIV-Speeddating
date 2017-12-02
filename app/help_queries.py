from app.models import Participants, TimeSlots, Events
from app import app

def get_list_women_of_slot(session, slot_id):
    w_in = []
    w_out = []

    try:
        slot = TimeSlots.query.filter(TimeSlots.id == slot_id).first()
        women = Participants.query.order_by(Participants.creation_timestamp).filter(
                Participants.available_slot == slot_id,
                Participants.gender == '1').all()
    except Exception as e:
        print(e)
        return e

    count = 0
    print("bla")
    for w in women:
        if w.confirmed == 1 and count < slot.nr_couples:
            count = count + 1
            w_in.append(w)
        else:
            w_out.append(w)
    return [w_in, w_out]


def get_list_men_of_slot(session, slot_id):
    m_in = []
    m_out = []

    try:
        slot = TimeSlots.query.filter(TimeSlots.id == slot_id).first()
        men = Participants.query.order_by(Participants.creation_timestamp).filter(
                Participants.available_slot == slot_id,
                Participants.gender == '0').all()
    except Exception as e:
        print(e)
        return e

    count = 0
    for m in men:
        if m.confirmed == 1 and count < slot.nr_couples:
            count = count + 1
            m_in.append(m)
        else:
            m_out.append(m)
    return [m_in, m_out]

def get_string_mails_of_list(session, slot, plist):
    mail = ""
    for p in plist:
        mail = mail + p.email + "; "
    return mail[:-2]

def get_string_of_date_list(date_list):
    dates_string = ''
    if date_list != None:
        for date in date_list:
            dates_string = dates_string + str(date.strftime("%d. %B, "))
        dates_string = dates_string[:-2]
    return dates_string
