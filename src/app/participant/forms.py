__author__ = 'alex'
from wtforms import Form, StringField, SelectField, TextAreaField


class ParticipantsForm(Form):
    name = StringField('Name')