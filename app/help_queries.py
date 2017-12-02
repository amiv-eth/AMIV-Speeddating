"""
Collection of frequently used queries
"""
from app.models import Participants, TimeSlots

def get_list_women_of_slot(session, slot_id):
    """ Returns two lists, one with the women in the slot, one with the women not in the slot """
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
    for woman in women:
        if woman.confirmed == 1 and count < slot.nr_couples:
            count = count + 1
            w_in.append(woman)
        else:
            w_out.append(woman)
    return [w_in, w_out]


def get_list_men_of_slot(session, slot_id):
    """ Returns two lists, one with the men in the slot, one with the men not in the slot """
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
    for man in men:
        if man.confirmed == 1 and count < slot.nr_couples:
            count = count + 1
            m_in.append(man)
        else:
            m_out.append(man)
    return [m_in, m_out]

def get_string_mails_of_list(session, slot, plist):
    """ Create list of email addresses as a string """
    mail = ""
    for p in plist:
        mail = mail + p.email + "; "
    return mail[:-2]


def get_string_of_date_list(date_list):
    """ Create list of timeslots as a string """
    dates_string = ''
    if date_list != None:
        for date in date_list:
            dates_string = dates_string + str(date.strftime("%d. %B, "))
        dates_string = dates_string[:-2]
    return dates_string
