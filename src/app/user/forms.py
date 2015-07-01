__author__ = 'Alex'
from wtforms import Form, StringField, validators


class SettingsForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    company_name = StringField('Company Name', [validators.Length(min=4, max=25)])