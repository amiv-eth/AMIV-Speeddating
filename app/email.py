"""
All e-mail sending is done through this file.
"""

from flask import url_for
from flask_mail import Message, BadHeaderError
from app import mail
from jinja2 import Environment, PackageLoader


def send_post_signup_email(participant):
    """Send e-mail to participant after successful signup
    
    Participants will receive an email containing links to confirm, edit or cancel their participation
    
    Arguments:
        participant {app.models.Participants} -- [the participant]
    """
    
    env = Environment(
        loader=PackageLoader('app.email', 'templates/email')
    )
    template = env.get_template('post_signup_email.j2')

    context = {
        'name': participant.Prename,
        'confirm_link': url_for('confirm_participation', confirm_token=participant.ConfirmToken, _external=True),
        'edit_link': url_for('edit_participation', edit_token=participant.EditToken, _external=True),
        'cancel_link': url_for('cancel_participation', cancel_token=participant.CancelToken, _external=True),
    }

    msg = Message(
        html=template.render(**context),
        subject='Deine AMIV-Speeddating Anmeldung',
        recipients=[participant.EMail])
    try:
        mail.send(msg)
    except BadHeaderError as e:
        print('A BadHeaderError ocurred')
