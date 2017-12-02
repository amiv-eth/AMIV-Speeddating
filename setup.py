"""
Creates database schema and adds admin
"""

import argparse
from app import bcrypt, db
from app.models import AdminUser

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('admin_username')
parser.add_argument('admin_password')
args = parser.parse_args()

response = input('This will nuke your current database! Are you sure you want to continue? [y/n]')
if response != 'y':
    exit()

# Nuke db
print('Nuking database...')
db.drop_all()

# Create db
print('Creating schema...')
db.create_all()

# Create admin user
print('Creating admin user...')
admin_user = AdminUser()
admin_user.username = args.admin_username
admin_user.password = bcrypt.generate_password_hash(args.admin_password)
db.session.add(admin_user)
db.session.commit()

print('Done!')
