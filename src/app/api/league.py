from flask.ext.restful import Resource, reqparse, fields, marshal
from .base import api_auth
from ..user import User
from ..league.models import League


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
        super(LeagueListAPI, self).__init__()

    def get(self):
        """ return all leagues associated with the user """
        args = self.reqparse.parse_args()
        user_id = args['username']
        ancestor_key = User.build_key(user_id=user_id)

        leagues = League.query(ancestor=ancestor_key).fetch()
        return {'data': [marshal(l, league_template) for l in leagues]}

    def post(self):
        """ create a new league """
        pass


class LeagueAPI(Resource):
    decorators = [api_auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True, location='authorization')
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('rating_scheme', type=str, default="ELO", location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        super(LeagueAPI, self).__init__()

    def get(self, league_id):
        """ return the specified league """
        args = self.reqparse.parse_args()
        user_id = args['username']
        ancestor_key = User.build_key(user_id=user_id)

        league = League.build_key(league_id=league_id, user_key=ancestor_key).get()
        return {'data': marshal(league, league_template)}

    def put(self, league_id):
        """ update the specified league """
        pass

    def delete(self, league_id):
        """ delete the specified league """
        pass