from flask.ext.restful import Resource, reqparse
from .base import api_auth


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
        return {'your_id': user_id}

    def post(self):
        """ create a new league """
        pass


class LeagueAPI(Resource):
    def get(self, league_id):
        """ return the specified league """
        pass

    def put(self, league_id):
        """ update the specified league """
        pass

    def delete(self, league_id):
        """ delete the specified league """
        pass