# Checks a user's credentials
# TODO: This can probably be merged into models.py

from app import bcrypt
from app.models import AdminUser

def check_credentials(username, password):
    """ Looks for AdminUser with username, checks password """
    # Find the user in the database
    admin = AdminUser.query.filter_by(username=username).first()
    if admin is None:
        return False

    # Check password
    if bcrypt.check_password_hash(admin.password, password):
        return True
    return False
