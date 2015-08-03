from flask.ext.restful import fields, marshal
from app.api.base import BaseAuthResource
from app.league.models import LeagueModel, create_league, update_league, delete_league


league_template = {
    'league_id': fields.String,
    'name': fields.String,
    'rating_scheme': fields.String,
    'description': fields.String,
    'participant_count': fields.Integer
}


class LeagueListAPI(BaseAuthResource):
    OPTIONAL_ARGS = ['name', 'rating_scheme', 'description']

    def get(self):
        """ return all leagues associated with the user """
        leagues = LeagueModel.query(ancestor=self.user.key).fetch()
        return {'data': [marshal(l, league_template) for l in leagues]}

    def post(self):
        """ create a new league """
        new_league = create_league(self.user, self.args.get('name'), self.args.get('rating_scheme'),
                                   description=self.args.get('description'))
        return {'data': marshal(new_league, league_template)}


class LeagueAPI(BaseAuthResource):
    OPTIONAL_ARGS = ['name', 'rating_scheme', 'description']

    def get(self, league_id):
        """ return the specified league """
        league = LeagueModel.build_key(league_id=league_id, user_key=self.user.key).get()
        return {'data': marshal(league, league_template)}

    def put(self, league_id):
        """ update the specified league """
        updated_league = update_league(self.user, league_id, self.args.get('name'), self.args.get('rating_scheme'),
                                       description=self.args.get('description'))
        return {'data': marshal(updated_league, league_template)}

    def delete(self, league_id):
        """ delete the specified league """
        delete_league(self.user, league_id)
        return {'data': 'Success'}