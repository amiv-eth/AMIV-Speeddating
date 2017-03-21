from wtforms import Form, DateField, RadioField, StringField, IntegerField, PasswordField, validators
from wtforms_components import TimeField

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
