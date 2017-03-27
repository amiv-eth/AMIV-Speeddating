from main import Base

class Participants(Base):
    __tablename__ = 'Participants'
    
    id = Column(Integer, primary_key=True)
    DefSlot = Column(Integer, primary_key=False)
    AvailableSlot = Column(String(50), primary_key=False)
    EventID = Column(Integer, unique=False)
    Name = Column(String(80), unique=False)
    Prename = Column(String(80), unique=False)
    EMail = Column(String(120), unique=False)
    MobileNr = Column(String(20), unique=False)
    Address = Column(String(200), unique=False)
    Birthday = Column(Date, unique=False)
    Gender = Column(Integer, unique=False)
    StudyCourse = Column(String(80), unique=False)
    StudySemester = Column(String(80), unique=False)
    PerfectDate = Column(String(300), unique=False)
    Fruit = Column(String(300), unique=False)
    CreationTimestamp = Column(DateTime, unique=False)

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


class TimeSlots(Base):
    __tablename__ = 'TimeSlots'
    ID = Column(Integer, primary_key=True)
    EventID = Column(Integer, unique=False)
    Date = Column(Date, unique=False)
    StartTime = Column(DateTime, unique=False)
    EndTime = Column(DateTime, unique=False)
    NrCouples = Column(Integer, primary_key=False)
    AgeRange = Column(Integer, primary_key=False)

    def __init__(self, event_id, date, starttime, endtime, nrCouples, ageRange):
        self.EventID = event_id
        self.Date = date
        self.StartTime = starttime
        self.EndTime = endtime
        self.NrCouples = nrCouples
        self.AgeRange = ageRange


class Events(Base):
    __tablename__ = 'Events'
    ID = Column(Integer, primary_key=True)
    Name = Column(String(80), unique=False)
    Year = Column(Date, unique=False)
    Semester = Column(Integer, unique=False)
    CreationTimestamp = Column(DateTime, unique=False)
    SignupOpen = Column(Integer, unique=False)
    Active = Column(Integer, unique=False)

    def __init__(self, name, year, semester, timestamp, signup_open, active):
        self.Name = name
        self.Year = year
        self.Semester = semester
        self.CreationTimestamp = timestamp
        self.SignupOpen = signup_open
        self.Active = active
