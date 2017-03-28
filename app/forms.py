from wtforms import Form, TextField, DateField, RadioField, StringField, IntegerField, PasswordField, SelectField, validators
from wtforms_components import TimeField
from app.models import Participants, TimeSlots, Events

class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])


class CreateEventForm(Form):
    name = StringField('Name', [validators.DataRequired()])
    year = IntegerField('Year', [validators.DataRequired(), validators.NumberRange(min=1000, max=9999)])
    semester = RadioField('Semester:', [validators.DataRequired()], choices=[('0','FS'),('1','HS')])


class CreateTimeSlotForm(Form):
    date = DateField('Date',[validators.DataRequired()], format='%Y-%m-%d')
    starttime = TimeField('Start-Time', [validators.DataRequired()])
    endtime = TimeField('End-Time', [validators.DataRequired()])
    nrcouples = IntegerField('Nr of Couples', [validators.DataRequired(), validators.NumberRange(min=0, max=25)])
    agerange = RadioField('Age-Range:', [validators.DataRequired()], choices=[('0','<22'),('1','22 - 25'),('2','> 25')])


class SignupForm(Form):
    name = StringField('Nachname (*)', [validators.DataRequired()])
    prename = StringField('Vorname (*)', [validators.DataRequired()])
    email = TextField('E-Mail Adresse (*)', validators=[validators.DataRequired(), validators.Email()])
    mobilenr = StringField( 'Handynummer (*)', [validators.DataRequired()])
    address = TextField('Adresse (*)', [validators.DataRequired()])
    birthday = DateField('Geburtstag (*)',[validators.DataRequired()], format='%Y-%m-%d')
    gender = RadioField('Geschlecht (*)', [validators.DataRequired()], choices=[('1','w'),('0','m')])
    studycourse = StringField('Studiengang (*)', [validators.DataRequired()])
    studysemester = StringField('Semester (*)', [validators.DataRequired()])
    perfectdate = StringField('Das perfekte Date?', [validators.Optional()])
    fruit = StringField('Lieblingsfrucht?', [validators.Optional()])

    availableslots = RadioField('Verfügbare Daten (*) (Bitte achte auf die Altersgruppe)', validators = [validators.DataRequired()], coerce=int)
