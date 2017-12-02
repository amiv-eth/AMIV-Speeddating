"""
Handles participant side authentication using tokens
"""
from secrets import token_hex
from app import db
from app.email import send_post_signup_email
from app.models import Participants

def create_confirm_token(participant):
    """ Generates ConfirmToken and stores it in participant """
    participant.confirm_token = token_hex(32)
    db.session.commit()
    return participant.confirm_token

def create_edit_token(participant):
    """ Generates edit_token and stores it in participant """
    participant.edit_token = token_hex(32)
    db.session.commit()
    return participant.edit_token

def create_cancel_token(participant):
    """ Generates cancel_token and stores it in participant """
    participant.cancel_token = token_hex(32)
    db.session.commit()
    return participant.cancel_token

def post_signup(sender, **kwargs):
    """Post-signup hook

    Is called after a participant signs up. Takes care of token creation
    and email sending.
    """
    if 'participant' in kwargs:
        participant = kwargs['participant']
    else:
        # https://gitlab.ethz.ch/amiv/AMIV-Speeddating/issues/13
        return

    # Create tokens
    create_confirm_token(participant)
    create_edit_token(participant)
    create_cancel_token(participant)

    # Send email
    send_post_signup_email(participant)

def confirm_participation(confirm_token):
    " Check if confirm_token is valid and, if yes, sets Confirmed to True. "
    # Find Participant corresponding to token
    participant = Participants.query.filter_by(confirm_token=confirm_token).first()
    if participant is None:
        return False

    # Confirm Participant
    participant.confirmed = True
    db.session.commit()

    return True

def cancel_participation(cancel_token):
    " Check if cancel_token is valid and, if yes, sets Confirmed to False. "
    # Find Participant corresponding to token
    participant = Participants.query.filter_by(cancel_token=cancel_token).first()
    if participant is None:
        return False

    # Cancel Participant
    participant.confirmed = False
    db.session.commit()

    return True
