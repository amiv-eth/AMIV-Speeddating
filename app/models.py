"""
Contains model declarations for sqlalchemy.
"""
from datetime import date, datetime
from enum import Enum
from app import db
from app.signals import SIGNAL_REGISTRATION_OPENED, SIGNAL_REGISTRATION_CLOSED
from sqlalchemy import Column, Boolean, Integer, String, Text, Date, DateTime, Time, ForeignKey, Enum as EnumSQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin


class Gender(Enum):
    """ Enum type to represent gender information """
    MALE = 0
    FEMALE = 1

    def other(self):
        """ Return the other gender """
        return Gender(1 - self.value)

    @classmethod
    def choices(cls):
        """ Returns a list of all choices """
        return [(choice.value, choice.name) for choice in cls]

    def __str__(self):
        return str(self.value)


class Participants(db.Model):
    """Models a Participant"""
    __tablename__ = 'participants'

    id = Column(Integer, primary_key=True)
    slot = Column(Integer, ForeignKey('timeslots.id'), nullable=False)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)

    name = Column(String(80), unique=False)
    prename = Column(String(80), unique=False)
    email = Column(String(120), unique=False)
    mobile_nr = Column(String(20), unique=False)
    address = Column(String(200), unique=False)
    birthday = Column(Date, unique=False)
    gender = Column(EnumSQLAlchemy(Gender), unique=False)
    study_course = Column(String(80), unique=False)
    study_semester = Column(String(80), unique=False)
    perfect_date = Column(String(300), unique=False)
    fruit = Column(String(300), unique=False)
    creation_timestamp = Column(DateTime, unique=False)
    confirmed = Column(Boolean, unique=False)
    present = Column(Boolean, unique=False)
    paid = Column(Boolean, unique=False)
    date_nr = Column(Integer, unique=False)
    confirm_token = Column(String(64), unique=True)
    edit_token = Column(String(64), unique=True)
    cancel_token = Column(String(64), unique=True)
    likes = Column(String(64), unique=False)

    def __str__(self):
        return '{} {}'.format(self.prename, self.name)

    def __repr__(self):
        return self.__str__()

    def get_age(self):
        """ Calculate age """
        today = date.today()
        return today.year - self.birthday.year - ((today.month, today.day) <
                                                  (self.birthday.month, self.birthday.day))

    class AlreadySignedUpException(Exception):
        """ Raised if an attempt is made to sign up a Participant for the same Event twice """
        pass

    def __init__(self, *args, **kwargs):
        try:
            event_id = kwargs['event_id']
            email = kwargs['email']
        except KeyError as key_error:
            raise key_error

        participant = Participants.query.filter_by(
            event_id=event_id, email=email).first()
        if participant is not None:
            raise self.AlreadySignedUpException()
        super(Participants, self).__init__(*args, **kwargs)


class TimeSlots(db.Model):
    """Models a TimeSlot of an Event"""
    __tablename__ = 'timeslots'

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)

    date = Column(Date, unique=False)
    start_time = Column(Time, unique=False)
    end_time = Column(Time, unique=False)
    nr_couples = Column(Integer, primary_key=False)
    age_range = Column(Integer, primary_key=False)
    special_slot = Column(Boolean, unique=False)

    participants = relationship(
        'Participants', backref='timeslot', lazy='dynamic')

    def get_participants(self, on_waiting_list=None, **kwargs):
        """ Get list of participants that are signed up for the event
        in ascending order of creation_timestamp.
        Additional filtering can be done using keyword arguments.
        Optionally, the 'on_waiting_list' parameter allows to only show participants
        who 'made' the slot.
        """
        participants = self.participants.order_by(
            Participants.creation_timestamp)
        # Optional filtering by kwargs
        if kwargs is not None:
            participants = participants.filter_by(**kwargs)

        # Convert to list
        participant_list = participants.all()

        # Optional filtering by waiting list status
        if on_waiting_list is not None:
            if not on_waiting_list:
                return participant_list[:self.nr_couples]
            return participant_list[self.nr_couples:]

        return participant_list


class Semester(Enum):
    """ Enum type to represent the semester """
    HS = 0
    FS = 1


class Events(db.Model):
    """Models an Event and can include multiple TimeSlots"""
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=False)
    year = Column(Integer, unique=False)
    special_slots = Column(Boolean, unique=False)
    special_slots_name = Column(Text, unique=False)
    special_slots_description = Column(Text, unique=False)
    semester = Column(EnumSQLAlchemy(Semester), unique=False)
    creation_timestamp = Column(DateTime, unique=False)
    signup_open = Column(Boolean, unique=False)
    open_signup_timestamp = Column(DateTime, unique=False)
    close_signup_timestamp = Column(DateTime, unique=False)
    place = Column(String(80), unique=False)
    active = Column(Boolean, unique=False)
    participation_fee = Column(String(80), unique=False)

    participants = relationship(
        'Participants', backref='event', lazy='dynamic')
    slots = relationship('TimeSlots', backref='event', lazy='dynamic')

    def get_string_open_signup_timestamp(self, format):
        return str(self.open_signup_timestamp.strftime(format))

    def get_string_close_signup_timestamp(self, format):
        return str(self.close_signup_timestamp.strftime(format))

    def is_open(self):
        """ Check if we're in the signup timeslot
        Registration status should only be checked via this method.
        """

        if self.open_signup_timestamp <= datetime.now() and datetime.now() <= self.close_signup_timestamp:
            if not self.signup_open:
                SIGNAL_REGISTRATION_OPENED.send(self)
            self.signup_open = True
        else:
            if self.signup_open:
                SIGNAL_REGISTRATION_CLOSED.send(self)
            self.signup_open = False

        db.session.commit()
        return self.signup_open


class AdminUser(db.Model, UserMixin):
    """ Represents an admin user """
    __tablename__ = 'adminusers'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True)
    password = Column(String(60), unique=False)

    def get_id(self):
        return self.id
