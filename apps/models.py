from apps.database import db

class Participants(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    DefSlot = db.Column(db.Integer, primary_key=False)
    AvailableSlot = db.Column(db.String(50), primary_key=False)
    NonceConfirm = db.Column(db.String(50), primary_key=True)
    NonceCancel = db.Column(db.String(50), primary_key=True)
    Name = db.Column(db.String(80), unique=False)
    Prename = db.Column(db.String(80), unique=False)
    EMail = db.Column(db.String(120), unique=False)
    MobileNr = db.Column(db.Integer, unique=False)
    Address = db.Column(db.String(200), unique=False)
    Birthday = db.Column(db.Date, unique=False)
    Sexe = db.Column(db.Boolean, unique=False)
    EventYear = db.Column(db.Date, unique=False)
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

    def __init__(self, name, prename, email, mobileNr, address, birthday, sexe, year, dSlot=None, aSlot=None, nConfirm=None, nCancel=None, course=None, semester=None, perfDate=None, singleSince=None, onlineDating=None, pickup=None, women=None, men=None, advantages=None, nrDates=None, longestRel=None, findDates=None, fruit=None):
        self.DefSlot = dSlot
        self.AvailableSlot = aSlot
        self.NonceConfirm = nConfirm
        self.NonceCancel = nCancel
        self.Name = name
        self.Prename = prename
        self.EMail = email
        self.MobileNr = mobileNr
        self.Address = address
        self.Birthday = birthday
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
    EventYear = db.Column(db.Date, unique=True)
    Date = db.Column(db.Date, unique=True)
    StartTime = db.Column(db.Time, primary_key=True)
    EndTime = db.Column(db.Time, primary_key=True)
    NrCouples = db.Column(db.Integer, primary_key=False)

    def __init__(self, year, date, startDate, endTime, nrCouples):
        self.EventYear = year
        self.Date = date
        self.StartTime = startTime
        self.EndTime = endTime
        self.NrCouples = nrCouples
