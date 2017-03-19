from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Participants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    DefSlot = db.Column(db.Integer, primary_key=False)
    AvailableSlot = db.Column(db.String(50), primary_key=False)
    NonceConfirm = db.Column(db.String(50), primary_key=False)
    NonceCancel = db.Column(db.String(50), primary_key=False)
    Name = db.Column(db.String(80), unique=False)
    Prename = db.Column(db.String(80), unique=False)
    EMail = db.Column(db.String(120), unique=False)
    MobileNr = db.Column(db.String(20), unique=False)
    Address = db.Column(db.String(200), unique=False)
    Age = db.Column(db.Integer, unique=False)
    Sexe = db.Column(db.Boolean, unique=False)
    EventYear = db.Column(db.Integer, unique=False)
    StudyCourse = db.Column(db.String(80), unique=False)
    StudySemester = db.Column(db.String(80), unique=False)
    PerfectDate = db.Column(db.String(300), unique=False)
    SingleSince = db.Column(db.String(80), unique=False)
    OnlineDating = db.Column(db.String(300), unique=False)
    PickupLine = db.Column(db.String(300), unique=False)
    Women = db.Column(db.String(300), unique=False)
    Men = db.Column(db.String(300), unique=False)
    Advantages = db.Column(db.String(300), unique=False)
    NrDates = db.Column(db.String(300), unique=False)
    LongestRelationship = db.Column(db.String(300), unique=False)
    FindDates = db.Column(db.String(300), unique=False)
    Fruit = db.Column(db.String(300), unique=False)

    def __init__(self, name, prename, email, mobileNr, address, age, sexe, year=None, dSlot=None, aSlot=None, nConfirm=None, nCancel=None, course=None, semester=None, perfDate=None, singleSince=None, onlineDating=None, pickup=None, women=None, men=None, advantages=None, nrDates=None, longestRel=None, findDates=None, fruit=None):
        self.DefSlot = dSlot
        self.AvailableSlot = aSlot
        self.NonceConfirm = nConfirm
        self.NonceCancel = nCancel
        self.Name = name
        self.Prename = prename
        self.EMail = email
        self.MobileNr = mobileNr
        self.Address = address
        self.Age = age
        self.Sexe = sexe
        self.EventYear = year
        self.StudyCourse = course
        self.StudySemester = semester
        self.PerfectDate = perfDate
        self.SingleSince = singleSince
        self.OnlineDating = onlineDating
        self.PickupLine = pickup
        self.Women = women
        self.Men = men
        self.Advantages = advantages
        self.NrDates = nrDates
        self.LongestRelationship = longestRel
        self.FindDates = findDates
        self.Fruit = fruit


class TimeSlots(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    EventID = db.Column(db.Integer, unique=True)
    Date = db.Column(db.Date, unique=True)
    StartTime = db.Column(db.Time, primary_key=False)
    EndTime = db.Column(db.Time, primary_key=False)
    NrCouples = db.Column(db.Integer, primary_key=False)

    def __init__(self, event_id, date, startTime, endTime, nrCouples):
        self.EventID = event_id
        self.Date = date
        self.StartTime = startTime
        self.EndTime = endTime
        self.NrCouples = nrCouples


class Events(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), unique=False)
    Year = db.Column(db.Date, unique=False)
    Semester = db.Column(db.Boolean, unique=False)
    CreationTimestamp = db.Column(db.DateTime, unique=False)
    SignupOpen = db.Column(db.Boolean, unique=False)

    def __init__(self, name, year, semester, timestamp, signup_open):
        self.Name = name
        self.Year = year
        self.Semester = semester
        self.CreationTimestamp = timestamp
        self.SignupOpen = signup_open
