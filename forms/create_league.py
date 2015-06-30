__author__ = 'Alex'
from wtforms import Form, StringField, SelectField, TextAreaField


class CreateLeagueForm(Form):
    name = StringField('Name')
    rating_scheme = SelectField('Rating Scheme', choices=[('elo', 'ELO'), ('obj2', 'Type 2'), ('obj3', 'Type 3')])
    description = TextAreaField('Description')