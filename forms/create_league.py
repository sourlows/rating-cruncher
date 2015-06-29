__author__ = 'Alex'
from wtforms import Form, StringField, SelectField, TextAreaField


class CreateLeagueForm(Form):
    name = StringField('Name')
    rating_scheme = SelectField('Rating Scheme', choices=['ELO', 'Type 2', 'Type 3'])
    description = TextAreaField('Description')