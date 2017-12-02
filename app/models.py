from app.db import Model
from sqlalchemy import Column, Boolean, Integer, String, Text, Date, DateTime
from flask_login import UserMixin

class Participants(Model):
    """Models a Participant"""
    ID = Column(Integer, primary_key=True)
    DefSlot = Column(Integer, primary_key=False)
    AvailableSlot = Column(String(50), primary_key=False)
    EventId = Column(Integer, unique=False)
    Name = Column(String(80), unique=False)
    Prename = Column(String(80), unique=False)
    Email = Column(String(120), unique=True)
    MobileNr = Column(String(20), unique=False)
    Address = Column(String(200), unique=False)
    Birthday = Column(Date, unique=False)
    Gender = Column(Integer, unique=False)
    StudyCourse = Column(String(80), unique=False)
    StudySemester = Column(String(80), unique=False)
    PerfectDate = Column(String(300), unique=False)
    Fruit = Column(String(300), unique=False)
    CreationTimestamp = Column(DateTime, unique=False)
    Confirmed = Column(Integer, unique=False)
    Present = Column(Integer, unique=False)
    Payed = Column(Integer, unique=False)
    DateNr = Column(Integer, unique=False)
    ConfirmToken = Column(String(64), unique=True)
    EditToken = Column(String(64), unique=True)
    CancelToken = Column(String(64), unique=True)

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
                 confirmed=1,
                 present=0,
                 payed=0,
                 datenr=0):
        self.DefSlot = dSlot
        self.AvailableSlot = aSlot
        self.EventID = eventid
        self.Name = name
        self.Prename = prename
        self.EMail = email
        self.MobileNr = mobileNr
        self.Address = address
        self.Birthday = bday
        self.Gender = gender
        self.StudyCourse = course
        self.StudySemester = semester
        self.PerfectDate = perfDate
        self.Fruit = fruit
        self.CreationTimestamp = timestamp
        self.Confirmed = confirmed
        self.Present = present
        self.Payed = payed
        self.DateNr = datenr


class TimeSlots(Model):
    ID = Column(Integer, primary_key=True)
    EventID = Column(Integer, unique=False)
    Date = Column(Date, unique=False)
    StartTime = Column(DateTime, unique=False)
    EndTime = Column(DateTime, unique=False)
    NrCouples = Column(Integer, primary_key=False)
    AgeRange = Column(Integer, primary_key=False)
    SpecialSlot = Column(Boolean, unique=False)

    def __init__(self, event_id, date, starttime, endtime, nrCouples, ageRange,
                 specialslot):
        self.EventID = event_id
        self.Date = date
        self.StartTime = starttime
        self.EndTime = endtime
        self.NrCouples = nrCouples
        self.AgeRange = ageRange
        self.SpecialSlot = specialslot


class Events(Model):
    ID = Column(Integer, primary_key=True)
    Name = Column(String(80), unique=False)
    Year = Column(Date, unique=False)
    SpecialSlots = Column(Boolean, unique=False)
    SpecialSlotsName = Column(Text, unique=False)
    SpecialSlotsDescription = Column(Text, unique=False)
    Semester = Column(Boolean, unique=False)
    CreationTimestamp = Column(DateTime, unique=False)
    SignupOpen = Column(Boolean, unique=False)
    OpenSignupTimestamp = Column(DateTime, unique=False)
    CloseSignupTimestamp = Column(DateTime, unique=False)
    Place = Column(String(80), unique=False)
    Active = Column(Boolean, unique=False)
    ParticipationFee = Column(String(80), unique=False)

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
        self.Name = name
        self.Year = year
        self.SpecialSlots = specslot
        self.SpecialSlotsName = specslotname
        self.SpecialSlotsDescription = sepcslotdescription
        self.Place = place
        self.Semester = semester
        self.CreationTimestamp = timestamp
        self.SignupOpen = signup_open
        self.OpenSignupTimestamp = open_signup_timestamp
        self.CloseSignupTimestamp = close_signup_timestamp
        self.Active = active
        self.ParticipationFee = pfee

    def get_string_close_signup_timestamp(self, format):
        return str(self.CloseSignupTimestamp.strftime(format))


class AdminUser(Model, UserMixin):
    """ Represents an admin user """
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True)
    password = Column(String(60), unique=False)

    def get_id(self):
        return self.id
