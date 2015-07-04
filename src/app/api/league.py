from flask.ext.restful import Resource, reqparse, fields, marshal
from app.api.base import api_auth
from app.league.models import LeagueModel, create_league, update_league, delete_league
from app.user.models import UserModel


league_template = {
    'league_id': fields.String,
    'name': fields.String,
    'rating_scheme': fields.String,
    'description': fields.String,
}


class LeagueListAPI(Resource):
    decorators = [api_auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True, location='authorization')
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('rating_scheme', type=str, default="ELO", location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.args = self.reqparse.parse_args()
        self.user = UserModel.build_key(user_id=self.args['username']).get()
        super(LeagueListAPI, self).__init__()

    def get(self):
        """ return all leagues associated with the user """
        leagues = LeagueModel.query(ancestor=self.user.key).fetch()
        return {'data': [marshal(l, league_template) for l in leagues]}

    def post(self):
        """ create a new league """
        new_league = create_league(self.user, self.args.get('name'), self.args.get('rating_scheme'),
                                   description=self.args.get('description'))
        return {'data': marshal(new_league, league_template)}


class LeagueAPI(Resource):
    decorators = [api_auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True, location='authorization')
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('rating_scheme', type=str, default="ELO", location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.args = self.reqparse.parse_args()
        self.user = UserModel.build_key(user_id=self.args['username']).get()
        super(LeagueAPI, self).__init__()

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