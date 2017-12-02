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

# The participant_signals namespace contains all signals related to the participant side
participant_signals = Namespace()


from app import views, models, forms, signals, email, participants

# Connect signals
signals.new_signup.connect(participants.post_signup)
