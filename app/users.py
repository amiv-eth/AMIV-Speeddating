from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from app import app

class User(UserMixin):
    pass

def check_credentials(username, password):
    if username in app.config['USERS'].keys():
        if app.config['USERS'][username] == password:
            return True
    return False
