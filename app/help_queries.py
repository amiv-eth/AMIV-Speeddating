"""
Collection of frequently used queries
"""
from app.models import Participants


def participants_in_slot(slot, gender=None):
    """ Returns a list of two lists, one containing the participants who made the slot,
    one containing those on the waiting list """
    # Only select Participants who have confirmed their participation
    participants = Participants.query.filter(
        Participants.available_slot == slot.id,
        Participants.confirmed
    ).order_by(Participants.creation_timestamp)

    # Optional gender filtering
    if gender is not None:
        participants = participants.filter(Participants.gender == gender)

    participants_list = participants.all()
    nr_couples = slot.nr_couples

    # If there are more Participants than slots, only the first few will get in
    if len(participants_list) > nr_couples:
        return [participants_list[:nr_couples], participants_list[nr_couples:]]
    return [participants_list, []]


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
