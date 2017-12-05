"""
Contains all functions etc that help the signup view

"""

from app import db
from app.models import Participants, TimeSlots, Gender


def get_age_string_list():
    """ Return all defined age strings """

    age_strings = []
    age_strings.append('< 22'.ljust(6))
    age_strings.append('22-25'.ljust(6))
    age_strings.append('> 25'.ljust(6))
    age_strings.append('alle'.ljust(6))
    return age_strings


def get_slots_choices(timeslots):
    """ returns all timeslots as tupels of (id, description_string)
    in separate lists for normal timeslots and special_timeslots
    """

    ids_nonspecial = []
    ids_special = []
    strings_non_special = []
    strings_special = []

    age_strings = get_age_string_list()

    for slot in timeslots:
        if slot.special_slot == 1:
            ids_special.append(int(slot.id))
            nr_women = Participants.query.filter(
                Participants.available_slot == slot.id,
                Participants.confirmed is True,
                Participants.gender == Gender.FEMALE).count()
            nr_men = Participants.query.filter(
                Participants.available_slot == slot.id,
                Participants.confirmed is True,
                Participants.gender == Gender.MALE).count()
            stri = '&nbsp &nbsp &nbsp'
            stri = stri + \
                slot.date.strftime("%a %d. %b %y") + \
                '&nbsp &nbsp &nbsp'
            stri = str(stri).ljust(50, ' ' [0:1]) + str(
                slot.start_time)[:-3] + ' - ' + str(slot.end_time)[:-3]
            stri = stri + '&nbsp &nbsp &nbsp'
            stri = stri + 'Altersgruppe: &nbsp' + \
                age_strings[slot.age_range]
            stri = stri + '&nbsp &nbsp &nbsp Anmeldungsstand: &nbsp &nbsp  M: ' + \
                str(nr_men) + '/' + str(slot.nr_couples)
            stri = stri + '&nbsp &nbsp W: ' + \
                str(nr_women) + '/' + str(slot.nr_couples)
            strings_special.append(stri)
        elif slot.special_slot == 0:
            ids_nonspecial.append(int(slot.id))
            nr_women = Participants.query.filter(
                Participants.available_slot == slot.id,
                Participants.confirmed is True,
                Participants.gender == Gender.FEMALE).count()
            nr_men = Participants.query.filter(
                Participants.available_slot == slot.id,
                Participants.confirmed is True,
                Participants.gender == Gender.MALE).count()
            stri = '&nbsp &nbsp &nbsp'
            stri = stri + \
                slot.date.strftime("%a %d. %b %y") + \
                '&nbsp &nbsp &nbsp'
            stri = str(stri).ljust(50, ' ' [0:1]) + str(
                slot.start_time)[:-3] + ' - ' + str(slot.end_time)[:-3]
            stri = stri + '&nbsp &nbsp &nbsp'
            stri = stri + 'Altersgruppe: &nbsp' + \
                age_strings[slot.age_range]
            stri = stri + '&nbsp &nbsp &nbsp Anmeldungsstand: &nbsp &nbsp  M: ' + \
                str(nr_men) + '/' + str(slot.nr_couples)
            stri = stri + '&nbsp &nbsp W: ' + \
                str(nr_women) + '/' + str(slot.nr_couples)
            strings_non_special.append(stri)

    available_slots_choices = [(ids_nonspecial[i], strings_non_special[i])
                               for i in range(0, len(ids_nonspecial))]
    available_special_slots_choices = [(ids_special[i], strings_special[i])
                                       for i in range(0, len(ids_special))]

    return [available_slots_choices, available_special_slots_choices]


def check_if_mail_unique_within_event(email, event):
    """ return True if mail is unique within the event, else False """
    return Participants.query.filter_by(email=email, event_id=event.id).count() == 0
