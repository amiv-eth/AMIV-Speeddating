from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Participants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    DefSlot = db.Column(db.Integer, primary_key=False)
    AvailableSlot = db.Column(db.String(50), primary_key=False)
    EventID = db.Column(db.Integer, unique=False)
    Name = db.Column(db.String(80), unique=False)
    Prename = db.Column(db.String(80), unique=False)
    EMail = db.Column(db.String(120), unique=False)
    MobileNr = db.Column(db.String(20), unique=False)
    Address = db.Column(db.String(200), unique=False)
    Birthday = db.Column(db.Date, unique=False)
    Gender = db.Column(db.Integer, unique=False)
    StudyCourse = db.Column(db.String(80), unique=False)
    StudySemester = db.Column(db.String(80), unique=False)
    PerfectDate = db.Column(db.String(300), unique=False)
    Fruit = db.Column(db.String(300), unique=False)
    CreationTimestamp = db.Column(db.DateTime, unique=False)

    def __init__(self, timestamp, eventid, name, prename, email, mobileNr, address, bday, gender, dSlot=None, aSlot=None, course=None, semester=None, perfDate=None, fruit=None):
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


class TimeSlots(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    EventID = db.Column(db.Integer, unique=False)
    Date = db.Column(db.Date, unique=False)
    StartTime = db.Column(db.DateTime, unique=False)
    EndTime = db.Column(db.DateTime, unique=False)
    NrCouples = db.Column(db.Integer, primary_key=False)
    AgeRange = db.Column(db.Integer, primary_key=False)

    def __init__(self, event_id, date, starttime, endtime, nrCouples, ageRange):
        self.EventID = event_id
        self.Date = date
        self.StartTime = starttime
        self.EndTime = endtime
        self.NrCouples = nrCouples
        self.AgeRange = ageRange


class Events(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), unique=False)
    Year = db.Column(db.Date, unique=False)
    Semester = db.Column(db.Integer, unique=False)
    CreationTimestamp = db.Column(db.DateTime, unique=False)
    SignupOpen = db.Column(db.Integer, unique=False)
    Active = db.Column(db.Integer, unique=False)

    def __init__(self, name, year, semester, timestamp, signup_open, active):
        self.Name = name
        self.Year = year
        self.Semester = semester
        self.CreationTimestamp = timestamp
        self.SignupOpen = signup_open
        self.Active = active
