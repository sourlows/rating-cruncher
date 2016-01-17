from app.league.exceptions import LeagueNotFoundException, InvalidRatingSchemeException
from app.api.base import BaseAuthResource, StringArgument, IntegerArgument
from app.league.models import LeagueModel, create_league, update_league, delete_league
from flask.ext.restful_swagger import swagger
from flask_restful import fields, marshal

LEAGUE_TEMPLATE = {
    'league_id': fields.String,
    'name': fields.String,
    'rating_scheme': fields.String,
    'description': fields.String,
    'participant_count': fields.Integer,
    'k_sensitivity': fields.String,
    'k_factor_scaling': fields.Integer,
}


class LeagueListAPI(BaseAuthResource):
    ARGUMENTS = frozenset([
        StringArgument('name', required=True),
        StringArgument('rating_scheme'),
        StringArgument('k_sensitivity'),
        IntegerArgument('k_factor_scaling'),
        StringArgument('description'),
    ])

    @swagger.operation(
        notes='Some notes on the league api',
        responseClass='League',
        nickname='league',
        parameters=[
            {
                "name": "league_id",
                "description": "A unique indentifier for a league",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "body"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "Returned all the stuff"
            }
        ]
    )
    def get(self):
        """ return all leagues associated with the user """
        leagues = LeagueModel.query(ancestor=self.user.key).fetch()
        return [marshal(l, LEAGUE_TEMPLATE) for l in leagues]

    def post(self):
        """ create a new league """
        try:
            new_league = create_league(self.user, self.args.get('name'), self.args.get('rating_scheme'),
                                       self.args.get('k_sensitivity'), self.args.get('k_factor_scaling'),
                                       description=self.args.get('description'))
        except InvalidRatingSchemeException:
            return 'Invalid rating scheme %s' % self.args.get('rating_scheme'), 400
        return marshal(new_league, LEAGUE_TEMPLATE)


class LeagueAPI(BaseAuthResource):
    ARGUMENTS = frozenset([
        StringArgument('name'),
        StringArgument('rating_scheme'),
        StringArgument('description'),
    ])

    def get(self, league_id):
        """ return the specified league """
        league = LeagueModel.build_key(league_id=league_id, user_key=self.user.key).get()
        if not league:
            return 'League not found for league id %s' % league_id, 404
        return marshal(league, LEAGUE_TEMPLATE)

    def put(self, league_id):
        """ update the specified league """
        try:
            updated_league = update_league(self.user, league_id, self.args.get('name'), self.args.get('rating_scheme'),
                                           description=self.args.get('description'))
        except LeagueNotFoundException:
            return 'League not found for league id %s' % league_id, 404
        except InvalidRatingSchemeException:
            return 'Invalid rating scheme %s' % self.args.get('rating_scheme'), 400

        return marshal(updated_league, LEAGUE_TEMPLATE)

    def delete(self, league_id):
        """ delete the specified league """
        try:
            delete_league(self.user, league_id)
        except LeagueNotFoundException:
            return 'League not found', 404
        return {'data': 'Success'}
