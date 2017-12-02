from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_pyfile("./config.py")
app.secret_key = app.config['APP_SECRET']
db = SQLAlchemy(app)
login_manager = LoginManager(app)
csrf = CSRFProtect(app)

from app import views, models, forms