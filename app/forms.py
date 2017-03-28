from wtforms import Form, TextField, DateField, RadioField, StringField, IntegerField, PasswordField, SelectField, DateTimeField, validators
from wtforms_components import TimeField
from app.models import Participants, TimeSlots, Events

class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Passwort', [validators.DataRequired()])


class CreateEventForm(Form):
    name = StringField('Name', [validators.DataRequired()])
    year = IntegerField('Jahr', [validators.DataRequired(), validators.NumberRange(min=1000, max=9999)])
    semester = RadioField('Semester', [validators.DataRequired()], choices=[('0','FS'),('1','HS')])
    opensignuptimestamp = DateTimeField('Zeitpunkt der Oeffnung des Anmeldefensters', [validators.Optional()], format='%Y-%m-%dT%H:%M:%S')
    closesignuptimestamp = DateTimeField('Zeitpunkt der Schliessung des Anmeldefensters', [validators.Optional()], format='%Y-%m-%dT%H:%M:%S')
    place = StringField('Ort', [validators.DataRequired()])
    participationfee = StringField('Teilnahmegebühr', [validators.DataRequired()])

class CreateTimeSlotForm(Form):
    date = DateField('Datum',[validators.DataRequired()], format='%Y-%m-%d')
    starttime = TimeField('Start-Zeit', [validators.DataRequired()])
    endtime = TimeField('End-Zeit', [validators.DataRequired()])
    nrcouples = IntegerField('Anzahl Paare', [validators.DataRequired(), validators.NumberRange(min=0, max=25)])
    agerange = RadioField('Altersgruppe', [validators.DataRequired()], choices=[('0','<22'),('1','22 - 25'),('2','> 25')])


class SignupForm(Form):
    name = StringField('Nachname (*)', [validators.DataRequired()])
    prename = StringField('Vorname (*)', [validators.DataRequired()])
    email = TextField('E-Mail Adresse (*)', validators=[validators.DataRequired(), validators.Email()])
    mobilenr = StringField('Handynummer (*)', [validators.DataRequired()])
    address = TextField('Adresse (*)', [validators.DataRequired()])
    birthday = DateField('Geburtstag (*)',[validators.DataRequired()], format='%Y-%m-%d')
    gender = RadioField('Geschlecht (*)', [validators.DataRequired()], choices=[('1','w'),('0','m')])
    studycourse = StringField('Studiengang (*)', [validators.DataRequired()])
    studysemester = StringField('Semester (*)', [validators.DataRequired()])
    perfectdate = StringField('Das perfekte Date?', [validators.Optional()])
    fruit = StringField('Lieblingsfrucht?', [validators.Optional()])

    availableslots = RadioField('Verfügbare Daten (*) (Bitte achte auf die Altersgruppe)', validators = [validators.DataRequired()], coerce=int)
