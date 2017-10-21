from wtforms import Form, TextField, DateField, RadioField, StringField, IntegerField, PasswordField, SelectField, DateTimeField, validators, HiddenField
from wtforms_components import TimeField
from app.models import Participants, TimeSlots, Events
from wtforms.validators import ValidationError
from datetime import datetime

class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Passwort', [validators.DataRequired()])


class CreateEventForm(Form):
    name = StringField('Name', [validators.DataRequired()])
    year = IntegerField('Jahr', [validators.DataRequired(), validators.NumberRange(min=1000, max=9999)])
    semester = RadioField('Semester', [validators.DataRequired()], choices=[('0','FS'),('1','HS')])
    specialslot = RadioField('Add special type of timeslots', [validators.DataRequired()], choices=[('0','No'),('1','Yes')])
    specialslotname = TextField('Name of the special timeslots (e.g. "Blind Speeddating"')
    specialslotdescription =  TextField('Description of the special timeslots (will be shown on the startpage)')
    opensignuptimestamp = DateTimeField('Zeitpunkt der Oeffnung des Anmeldefensters', [validators.DataRequired()], format='%Y-%m-%dT%H:%M')
    closesignuptimestamp = DateTimeField('Zeitpunkt der Schliessung des Anmeldefensters', [validators.DataRequired()], format='%Y-%m-%dT%H:%M')
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
    birthday = StringField('Geburtstag (*)',[validators.DataRequired()], render_kw={"placeholder": "DD.MM.YYYY"})
    gender = RadioField('Geschlecht (*)', [validators.DataRequired()], choices=[('1','w'),('0','m')])
    studycourse = StringField('Studiengang (*)', [validators.DataRequired()])
    studysemester = StringField('Semester (*)', [validators.DataRequired()])
    perfectdate = StringField('Das perfekte Date?', [validators.Optional()])
    fruit = StringField('Lieblingsfrucht?', [validators.Optional()])

    availableslots = RadioField('Verfügbare Daten (*) (Bitte achte auf die Altersgruppe, pro Zeitfenster je 12 Damen und 12 Herren)', validators = [validators.DataRequired()], coerce=int)

    def validate_birthday(form, field):
        try:
            datetime.strptime(field.data, '%d.%m.%Y')
        except:
            raise ValidationError("Wrong date format, should be DD.MM.YYYY")


class ChangeDateNr(Form):
    datenr = IntegerField('DateNr (Unique pro Geschlecht!)', [validators.DataRequired(), validators.NumberRange(min=0, max=20)])
    participant_id = HiddenField('Teilnehmer ID', [validators.DataRequired()])
