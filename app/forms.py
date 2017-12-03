"""
All forms are in this file.
"""
from datetime import datetime
from wtforms import TextField, DateField, RadioField, StringField, IntegerField, PasswordField,\
                    DateTimeField, validators, HiddenField, widgets, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Regexp
from wtforms_components import TimeField
from flask_wtf import FlaskForm


class MultiCheckboxField(SelectMultipleField):
    """ Field containing multiple checkboxes. """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class LoginForm(FlaskForm):
    """ Login form """
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Passwort', [validators.DataRequired()])


class CreateEventForm(FlaskForm):
    """ For admins to create an event """
    name = StringField('Name', [validators.DataRequired()])
    year = IntegerField('Jahr', [
        validators.DataRequired(),
        validators.NumberRange(min=1000, max=9999)
    ])
    semester = RadioField(
        'Semester', [validators.DataRequired()],
        choices=[('0', 'FS'), ('1', 'HS')])
    specialslot = RadioField(
        'Add special type of timeslots', [validators.DataRequired()],
        choices=[('0', 'No'), ('1', 'Yes')])
    specialslotname = TextField(
        'Name of the special timeslots (e.g. "Blind Speeddating"')
    specialslotdescription = TextField(
        'Description of the special timeslots (will be shown on the startpage)'
    )
    opensignuptimestamp = DateTimeField(
        'Zeitpunkt der Oeffnung des Anmeldefensters',
        [validators.DataRequired()],
        format='%Y-%m-%dT%H:%M')
    closesignuptimestamp = DateTimeField(
        'Zeitpunkt der Schliessung des Anmeldefensters',
        [validators.DataRequired()],
        format='%Y-%m-%dT%H:%M')
    place = StringField('Ort', [validators.DataRequired()])
    participationfee = StringField('Teilnahmegebühr',
                                   [validators.DataRequired()])


class CreateTimeSlotForm(FlaskForm):
    """ For admins to create a new time slot """
    date = DateField('Datum', [validators.DataRequired()], format='%Y-%m-%d')
    starttime = TimeField('Start-Zeit', [validators.DataRequired()])
    endtime = TimeField('End-Zeit', [validators.DataRequired()])
    nrcouples = IntegerField(
        'Anzahl Paare',
        [validators.DataRequired(),
         validators.NumberRange(min=0, max=25)])
    agerange = RadioField(
        'Altersgruppe', [validators.DataRequired()],
        choices=[('0', '<22'), ('1', '22 - 25'), ('2', '> 25'),
                 ('3', 'does not matter')])
    specialslot = RadioField(
        'Spezieller Timeslot', [validators.DataRequired()],
        choices=[('0', 'No'), ('1', 'Yes')])


class SignupForm(FlaskForm):
    """ For participants to sign up """
    name = StringField('Nachname (*)', [validators.DataRequired()])
    prename = StringField('Vorname (*)', [validators.DataRequired()])
    email = TextField(
        'E-Mail Adresse (*)',
        validators=[validators.DataRequired(),
                    validators.Email()])
    mobilenr = StringField('Handynummer (*)', [validators.DataRequired()])
    address = TextField('Adresse (*)', [validators.DataRequired()])
    birthday = StringField(
        'Geburtstag (*)', [validators.DataRequired()],
        render_kw={
            "placeholder": "DD.MM.YYYY"
        })
    gender = RadioField(
        'Geschlecht (*)', [validators.DataRequired()],
        choices=[('1', 'w'), ('0', 'm')])
    studycourse = StringField('Studiengang (*)', [validators.DataRequired()])
    studysemester = StringField('Semester (*)', [validators.DataRequired()])
    perfectdate = StringField('Das perfekte Date?', [validators.Optional()])
    fruit = StringField('Lieblingsfrucht?', [validators.Optional()])

    availableslots = MultiCheckboxField(
        'Verfügbare Daten (*)<br> <span class="notbold">(Bitte achte auf die Altersgruppe und die\
        Anzahl der bereits angemeldeten Personen (# angemeldete Personen) / (# verfügbare Plätze)\
        </span>',
        validators=[validators.Optional()],
        coerce=int)
    availablespecialslots = MultiCheckboxField(
        'Verfügbare Daten <span class="text-danger">Spezial Speeddating</span> (siehe Beschreibung\
        auf der Startseite) (*) <br> <span class="notbold">(Bitte achte auf die Altersgruppe und\
        die Anzahl der bereits angemeldeten Personen (# angemeldete Personen) / (# verfügbare\
        Plätze))</span>',
        validators=[validators.Optional()],
        coerce=int)

    def validate_availableslots(form, field):
        """ Makes sure that at exactly one event is selected. """
        if form.availableslots.data and form.availablespecialslots.data:
            raise ValidationError(
                'Du kannst dich für genau einen Termin anmelden')
        if not form.availableslots.data and not form.availablespecialslots.data:
            raise ValidationError(
                'Du musst dich für genau einen Termin anmelden')
        if len(form.availableslots.data) != 1 and len(
                form.availablespecialslots.data) != 1:
            raise ValidationError(
                'Du musst dich für genau einen Termin anmelden')

    def validate_availablespecialslots(form, field):
        """ Makes sure that at exactly one event is selected. """
        if form.availableslots.data and form.availablespecialslots.data:
            raise ValidationError(
                'Du kannst dich für genau einen Termin anmelden')
        if (not form.availableslots.data
            ) and not (form.availablespecialslots.data):
            raise ValidationError(
                'Du musst dich für genau einen Termin anmelden')
        if len(form.availableslots.data) != 1 and len(
                form.availablespecialslots.data) != 1:
            raise ValidationError(
                'Du musst dich für genau einen Termin anmelden')

    def validate_birthday(form, field):
        """ Make sure the birthday field is a valid date """
        try:
            datetime.strptime(field.data, '%d.%m.%Y')
        except:
            raise ValidationError("Falsches Datum Format: DD.MM.YYYY")

    def validate_on_submit(form, field):
        if (not form.availableslots.data) and not form.availablespecialslots.data:
            raise ValidationError(
                'Du musst dich für genau einen Termin anmelden')


class DateNrChangeForm(FlaskForm):
    """ Update the date number """
    datenr = IntegerField(
        'DateNr (Unique pro Geschlecht!)',
        [validators.DataRequired(),
         validators.NumberRange(min=0, max=20)])
    participant_id = HiddenField('Teilnehmer ID', [validators.DataRequired()])


class LikeForm(FlaskForm):
    """ Represents a form to update a participant's likes """
    likes = StringField('Likes', validators=[Regexp(r'^(\d+(,\d+)*)?$')])

class SendMatchesForm(FlaskForm):
    """ Allows an admin to send out matches via email """
    pass
