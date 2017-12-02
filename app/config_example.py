APP_SECRET = b'\x0cJ\xf6Q\x1a0\xba\xfb3? \xab\xe7\xfdv\x9c\x985\xf4\xe5o\x0e\x18\xe0'
## should be newly generated with:
## >>> import os
## >>> os.urandom(24)

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username1:password1@serverip/databasename'

# Disable flask-sqlalchemy's event system as we don't need it
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask-Mail config
MAIL_SERVER = 'smtp.ee.ethz.ch'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_DEFAULT_SENDER = 'speeddating@amiv.ethz.ch'
