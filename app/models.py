from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Participants(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    DefSlot = db.Column(db.Integer, primary_key=False)
    AvailableSlot = db.Column(db.String(50), primary_key=False)
    EventID = db.Column(db.Integer, unique=False)
    Name = db.Column(db.String(80), unique=False)
    Prename = db.Column(db.String(80), unique=False)
    EMail = db.Column(db.String(120), unique=True)
    MobileNr = db.Column(db.String(20), unique=False)
    Address = db.Column(db.String(200), unique=False)
    Birthday = db.Column(db.Date, unique=False)
    Gender = db.Column(db.Integer, unique=False)
    StudyCourse = db.Column(db.String(80), unique=False)
    StudySemester = db.Column(db.String(80), unique=False)
    PerfectDate = db.Column(db.String(300), unique=False)
    Fruit = db.Column(db.String(300), unique=False)
    CreationTimestamp = db.Column(db.DateTime, unique=False)
    Confirmed = db.Column(db.Integer, unique=False)
    Present = db.Column(db.Integer, unique=False)
    Payed = db.Column(db.Integer, unique=False)
    DateNr = db.Column(db.Integer, unique=False)

    def __init__(self, timestamp, eventid, name, prename, email, mobileNr, address, bday, gender, dSlot=None, aSlot=None, course=None, semester=None, perfDate=None, fruit=None, confirmed=1, present=0, payed=0, datenr=0):
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


class TimeSlots(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    EventID = db.Column(db.Integer, unique=False)
    Date = db.Column(db.Date, unique=False)
    StartTime = db.Column(db.DateTime, unique=False)
    EndTime = db.Column(db.DateTime, unique=False)
    NrCouples = db.Column(db.Integer, primary_key=False)
    AgeRange = db.Column(db.Integer, primary_key=False)
    SpecialSlot = db.Column(db.Boolean, unique=False)

    def __init__(self, event_id, date, starttime, endtime, nrCouples, ageRange, specialslot):
        self.EventID = event_id
        self.Date = date
        self.StartTime = starttime
        self.EndTime = endtime
        self.NrCouples = nrCouples
        self.AgeRange = ageRange
        self.SpecialSlot = specialslot

class Events(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), unique=False)
    Year = db.Column(db.Date, unique=False)
    SpecialSlots = db.Column(db.Boolean, unique=False)
    SpecialSlotsName = db.Column(db.Text, unique=False)
    SpecialSlotsDescription = db.Column(db.Text, unique=False)
    Semester = db.Column(db.Boolean, unique=False)
    CreationTimestamp = db.Column(db.DateTime, unique=False)
    SignupOpen = db.Column(db.Boolean, unique=False)
    OpenSignupTimestamp = db.Column(db.DateTime, unique=False)
    CloseSignupTimestamp = db.Column(db.DateTime, unique=False)
    Place = db.Column(db.String(80), unique=False)
    Active = db.Column(db.Boolean, unique=False)
    ParticipationFee = db.Column(db.String(80), unique=False)

    def __init__(self, name, year, specslot, specslotname, sepcslotdescription, semester, timestamp, signup_open, active, pfee, open_signup_timestamp=None, close_signup_timestamp=None):
        self.Name = name
        self.Year = year
        self.SpecialSlots = specslot
        self.SpecialSlotsName = specslotname
        self.SpecialSlotsDescription = sepcslotdescription
        self.Semester = semester
        self.CreationTimestamp = timestamp
        self.SignupOpen = signup_open
        self.OpenSignupTimestamp = open_signup_timestamp
        self.CloseSignupTimestamp = close_signup_timestamp
        self.Active = active
        self.ParticipationFee = pfee