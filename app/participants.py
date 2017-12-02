"""
Handles participant side authentication using tokens
"""
from secrets import token_hex
from app import db
from app.email import send_post_signup_email
from app.models import Participants

def create_confirm_token(participant):
    " Generates ConfirmToken and stores it in participant "
    participant.ConfirmToken = token_hex(32)
    db.session.commit()
    return participant.ConfirmToken

def create_edit_token(participant):
    " Generates EditToken and stores it in participant "
    participant.EditToken = token_hex(32)
    db.session.commit()
    return participant.EditToken

def create_cancel_token(participant):
    " Generates CancelToken and stores it in participant "
    participant.CancelToken = token_hex(32)
    db.session.commit()
    return participant.CancelToken

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
    participant = Participants.query.filter_by(ConfirmToken=confirm_token).first()
    if participant is None:
        return False

    # Confirm Participant
    participant.Confirmed = True
    db.session.commit()

    return True

def cancel_participation(cancel_token):
    " Check if cancel_token is valid and, if yes, sets Confirmed to False. "
    # Find Participant corresponding to token
    participant = Participants.query.filter_by(CancelToken=cancel_token).first()
    if participant is None:
        return False

    # Cancel Participant
    participant.Confirmed = False
    db.session.commit()

    return True
