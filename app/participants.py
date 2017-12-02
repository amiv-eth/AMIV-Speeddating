"""
Handles participant side authentication using tokens
"""
from secrets import token_hex
from app import db
from app.email import send_post_signup_email
from app.models import Participants

def create_confirm_token(participant):
    participant.ConfirmToken = token_hex(32)
    db.session.commit()
    return participant.ConfirmToken
    
def create_edit_token(participant):
    participant.EditToken = token_hex(32)
    db.session.commit()
    return participant.EditToken

def create_cancel_token(participant):
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
        # TODO: Notify admin via email
        # https://gitlab.ethz.ch/amiv/AMIV-Speeddating/issues/13
        return

    # Create tokens
    confirm_token = create_confirm_token(participant)
    edit_token = create_edit_token(participant)
    cancel_token = create_cancel_token(participant)

    # Send email
    send_post_signup_email(participant)

def confirm_participation(confirm_token):
    # Find Participant corresponding to token
    p = Participants.query.filter_by(ConfirmToken=confirm_token).first()
    if p is None:
        return False

    # Confirm Participant
    p.Confirmed = True
    db.session.commit()

    return True

def edit_participation(edit_token):
    # Find Participant corresponding to token
    return Participants.query.filter_by(EditToken=edit_token).first()

def cancel_participation(cancel_token):
    # Find Participant corresponding to token
    p = Participants.query.filter_by(CancelToken=cancel_token).first()
    if p is None:
        return False

    # Cancel Participant
    p.Confirmed = False
    db.session.commit()

    return True