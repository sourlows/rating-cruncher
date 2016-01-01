from wtforms import Form, StringField, SelectField, TextAreaField


class LeagueForm(Form):
    name = StringField('Name')
    rating_scheme = SelectField('Rating Scheme', choices=[('ELO', 'elo'), ('Label2', 'type2'), ('Label3', 'type3')])
    description = TextAreaField('Description')
