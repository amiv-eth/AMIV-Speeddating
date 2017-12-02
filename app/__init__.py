from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_pyfile("./config.py")
app.secret_key = app.config['APP_SECRET']
db = SQLAlchemy(app)
login_manager = LoginManager(app)
csrf = CSRFProtect(app)

# Provides secure password handling
bcrypt = Bcrypt(app)
# Prevent problems with excessively long passwords
# Will probably never happen but better to be safe
BCRYPT_HANDLE_LONG_PASSWORDS = True

from app import views, models, forms