#!/usr/bin/env python3

from apps.database import db
from apps.models import Participants, TimeSlots

from main import create_app
app = create_app()

with app.app_context():
        db.create_all()
