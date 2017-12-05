"""
The AMIV-Speeddating web application
https://gitlab.ethz.ch/amiv/AMIV-Speeddating
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from blinker import Namespace

app = Flask(__name__)
app.config.from_pyfile("./config.py")
app.secret_key = app.config['APP_SECRET']
db = SQLAlchemy(app)

login_manager = LoginManager(app)
csrf = CSRFProtect(app)

# Flask-Mail
mail = Mail(app)

# Provides secure password handling
bcrypt = Bcrypt(app)
# Prevent problems with excessively long passwords
# Will probably never happen but better to be safe
BCRYPT_HANDLE_LONG_PASSWORDS = True

# Contains signals related to the participant side
participant_signals = Namespace()

# Contains signals related to Events and TimeSlots
event_signals = Namespace()


from app import views
from app.admin import registration_opened, registration_closed
from app.signals import SIGNAL_NEW_SIGNUP, SIGNAL_REGISTRATION_OPENED, SIGNAL_REGISTRATION_CLOSED
from app.participants import post_signup

# Connect signals
SIGNAL_NEW_SIGNUP.connect(post_signup)
SIGNAL_REGISTRATION_OPENED.connect(registration_opened)
SIGNAL_REGISTRATION_CLOSED.connect(registration_closed)
