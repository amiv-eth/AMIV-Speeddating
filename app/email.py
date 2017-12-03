"""
All e-mail sending is done through this file.
"""

import logging
from flask import url_for
from flask_mail import Message, BadHeaderError
from app import mail
from jinja2 import Environment, PackageLoader

logging.basicConfig(filename='logging/email.log', level=logging.INFO)

def send_post_signup_email(participant):
    """Send e-mail to participant after successful signup

    Participants will receive an email containing links to confirm or cancel their participation

    Arguments:
        participant {app.models.Participants} -- [the participant]
    """
    env = Environment(
        loader=PackageLoader('app.email', 'templates/email')
    )
    template = env.get_template('post_signup_email.html')

    context = {
        'name': participant.prename,
        'confirm_link': url_for('confirm_participation',
                                confirm_token=participant.confirm_token,
                                _external=True),
        'cancel_link': url_for('cancel_participation',
                               cancel_token=participant.cancel_token,
                               _external=True),
    }

    msg = Message(
        html=template.render(**context),
        subject='Deine AMIV-Speeddating Anmeldung',
        recipients=[participant.email])
    try:
        mail.send(msg)
        logging.info('E-Mail sent to {}'.format(participant.email))
    except BadHeaderError:
        logging.error('Failed to send e-mail to {}: BadHeaderError'.format(participant.email))
