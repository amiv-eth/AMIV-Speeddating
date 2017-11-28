from app.models import Participants, TimeSlots, Events
from app import app

def get_list_women_of_slot(session, slot_id):
    w_in = []
    w_out = []

    try:
        slot = TimeSlots.query.filter(TimeSlots.ID == slot_id).first()
        women = Participants.query.order_by(Participants.CreationTimestamp).filter(
                Participants.AvailableSlot == slot_id,
                Participants.Gender == '1').all()
    except Exception as e:
        print(e)
        return e

    count = 0
    for w in women:
        if w.Confirmed == 1 and count < slot.NrCouples:
            count = count + 1
            w_in.append(w)
        else:
            w_out.append(w)
    return [w_in, w_out]


def get_list_men_of_slot(session, slot_id):
    m_in = []
    m_out = []

    try:
        slot = TimeSlots.query.filter(TimeSlots.ID == slot_id).first()
        men = Participants.query.order_by(Participants.CreationTimestamp).filter(
                Participants.AvailableSlot == slot_id,
                Participants.Gender == '0').all()
    except Exception as e:
        print(e)
        return e

    count = 0
    for m in men:
        if m.Confirmed == 1 and count < slot.NrCouples:
            count = count + 1
            m_in.append(m)
        else:
            m_out.append(m)
    return [m_in, m_out]

def get_string_mails_of_list(session, slot, plist):
    mail = ""
    for p in plist:
        mail = mail + p.EMail + "; "
    return mail[:-2]


