"""
All e-mail sending is done through this file.
"""

import logging
from logging.handlers import SMTPHandler
from flask import url_for
from flask_mail import Message, BadHeaderError
from app import app, mail
from jinja2 import Environment, PackageLoader

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# File handler will log everything except debug
file_handler = logging.FileHandler('app/logging/email.log')
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)

# E-Mail handler will only handle warnings and worse
email_handler = SMTPHandler(
    mailhost='{}:{}'.format(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
    fromaddr=app.config['MAIL_DEFAULT_SENDER'],
    toaddrs=app.config['MAIL_ADMINS'],
    subject='[AMIV-Speeddating] Issue',
    credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']))
email_handler.setLevel(logging.WARNING)
logger.addHandler(email_handler)

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
