__author__ = 'Alex'
from wtforms import Form, StringField, validators


class SettingsForm(Form):
    first_name = StringField('First Name', [validators.Length(min=4, max=25)])
    last_name = StringField('Last Name', [validators.Length(min=4, max=25)])