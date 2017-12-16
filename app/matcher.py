"""
A tool which automatically computes matches between participants and exchanges contact data
"""
from app import db
from app.models import Participants, TimeSlots
from app.email import send_matches_email

def find_matches(timeslot_id):
    """ Finds all matches of a given timeslot """
    matches = []
    slot = TimeSlots.get_or_404(timeslot_id)
    participants = slot.participants

    for participant in participants:
        target_gender = participant.gender.other()
        interest_ids = participant.likes.split(',')
        # Iterate over participant's interests
        for interest_id in interest_ids:
            interest = Participants.query.filter_by(date_nr=interest_id, gender=target_gender).first()
            if interest is None:
                break
            # Check if the interest is interested too
            interest_like_ids = interest.likes.split(',')
            if str(participant.date_nr) in interest_like_ids:
                matches.append((participant, interest))
    return matches

def inform_matches(matches):
    """ Informs each participant of their matches, but only if there is at least one match. """
    # matches is list of tuples
    # matches_ordered is dict of lists
    matches_ordered = {}
    for match in matches:
        if match[0] not in matches_ordered.keys():
            matches_ordered[match[0]] = []
        matches_ordered[match[0]].append(match[1])
    
    for participant, matches in matches_ordered.items():
        send_matches_email(participant, matches)
