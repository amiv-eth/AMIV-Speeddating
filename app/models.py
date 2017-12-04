"""
Contains model declarations for sqlalchemy.
"""
from datetime import date
from enum import Enum
from app import db
from sqlalchemy import Column, Boolean, Integer, String, Text, Date, DateTime, Time, Enum as EnumSQLAlchemy
from flask_login import UserMixin

class Gender(Enum):
    """ Enum type to represent gender information """
    MALE = 0
    FEMALE = 1
    def other(self):
        """ Return the other gender """
        return Gender(1 - self.value)

class Participants(db.Model):
    """Models a Participant"""
    id = Column(Integer, primary_key=True)
    def_slot = Column(Integer, primary_key=False)
    available_slot = Column(String(50), primary_key=False)
    event_id = Column(Integer, unique=False)
    name = Column(String(80), unique=False)
    prename = Column(String(80), unique=False)
    email = Column(String(120), unique=True)
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

    def __init__(self,
                 timestamp,
                 eventid,
                 name,
                 prename,
                 email,
                 mobileNr,
                 address,
                 bday,
                 gender,
                 dSlot=None,
                 aSlot=None,
                 course=None,
                 semester=None,
                 perfDate=None,
                 fruit=None,
                 confirmed=True,
                 present=False,
                 paid=False,
                 datenr=0):
        self.def_slot = dSlot
        self.available_slot = aSlot
        self.event_id = eventid
        self.name = name
        self.prename = prename
        self.email = email
        self.mobile_nr = mobileNr
        self.address = address
        self.birthday = bday
        self.gender = gender
        self.study_course = course
        self.study_semester = semester
        self.perfect_date = perfDate
        self.fruit = fruit
        self.creation_timestamp = timestamp
        self.confirmed = confirmed
        self.present = present
        self.paid = paid
        self.date_nr = datenr

    def __str__(self):
        return '{} {}'.format(self.prename, self.name)

    def __repr__(self):
        return self.__str__()

    def get_age(self):
        """ Calculate age """
        today = date.today()
        return today.year - self.birthday.year - ((today.month, today.day) <
                                                  (self.birthday.month, self.birthday.day))


class TimeSlots(db.Model):
    """Models a TimeSlot of an Event"""
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, unique=False)
    date = Column(Date, unique=False)
    start_time = Column(Time, unique=False)
    end_time = Column(Time, unique=False)
    nr_couples = Column(Integer, primary_key=False)
    age_range = Column(Integer, primary_key=False)
    special_slot = Column(Boolean, unique=False)

    def __init__(self, event_id, date, starttime, endtime, nrCouples, ageRange,
                 specialslot):
        self.event_id = event_id
        self.date = date
        self.start_time = starttime
        self.end_time = endtime
        self.nr_couples = nrCouples
        self.age_range = ageRange
        self.special_slot = specialslot


class Events(db.Model):
    """Models an Event and can include multiple TimeSlots"""
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=False)
    year = Column(Integer, unique=False)
    special_slots = Column(Boolean, unique=False)
    special_slots_name = Column(Text, unique=False)
    special_slots_description = Column(Text, unique=False)
    semester = Column(Boolean, unique=False)
    creation_timestamp = Column(DateTime, unique=False)
    signup_open = Column(Boolean, unique=False)
    open_signup_timestamp = Column(DateTime, unique=False)
    close_signup_timestamp = Column(DateTime, unique=False)
    place = Column(String(80), unique=False)
    active = Column(Boolean, unique=False)
    participation_fee = Column(String(80), unique=False)

    def __init__(self,
                 name,
                 year,
                 specslot,
                 specslotname,
                 sepcslotdescription,
                 place,
                 semester,
                 timestamp,
                 signup_open,
                 active,
                 pfee,
                 open_signup_timestamp=None,
                 close_signup_timestamp=None):
        self.name = name
        self.year = year
        self.special_slots = specslot
        self.special_slots_name = specslotname
        self.special_slots_description = sepcslotdescription
        self.place = place
        self.semester = semester
        self.creation_timestamp = timestamp
        self.signup_open = signup_open
        self.open_signup_timestamp = open_signup_timestamp
        self.close_signup_timestamp = close_signup_timestamp
        self.active = active
        self.participation_fee = pfee

    def get_string_close_signup_timestamp(self, format):
        return str(self.close_signup_timestamp.strftime(format))


class AdminUser(db.Model, UserMixin):
    """ Represents an admin user """
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True)
    password = Column(String(60), unique=False)

    def get_id(self):
        return self.id
