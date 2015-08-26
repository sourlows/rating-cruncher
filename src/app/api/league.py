from app.league.exceptions import LeagueNotFound, InvalidRatingScheme
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
        return [marshal(l, league_template) for l in leagues]

    def post(self):
        """ create a new league """
        try:
            new_league = create_league(self.user, self.args.get('name'), self.args.get('rating_scheme'),
                                       description=self.args.get('description'))
        except ValueError:
            return 'Invalid rating scheme.', 400
        return [marshal(new_league, league_template)]


class LeagueAPI(BaseAuthResource):
    OPTIONAL_ARGS = ['name', 'rating_scheme', 'description']

    def get(self, league_id):
        """ return the specified league """
        league = LeagueModel.build_key(league_id=league_id, user_key=self.user.key).get()
        if not league:
            return 'Invalid league.', 404
        return marshal(league, league_template)

    def put(self, league_id):
        """ update the specified league """
        try:
            updated_league = update_league(self.user, league_id, self.args.get('name'), self.args.get('rating_scheme'),
                                           description=self.args.get('description'))
        except ValueError:
            return 'Invalid league id.', 404
        except LeagueNotFound:
            return ["No league found for id" + league_id], 404
        except InvalidRatingScheme:
            return 'Invalid rating scheme.', 400

        return marshal(updated_league, league_template)

    def delete(self, league_id):
        """ delete the specified league """
        try:
            delete_league(self.user, league_id)
        except LeagueNotFound:
            return 'League not found', 404
        return {'data': 'Success'}