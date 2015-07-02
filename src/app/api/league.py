from flask.ext.restful import Resource, reqparse


class LeagueListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('rating_scheme', type=str, default="ELO", location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        super(LeagueListAPI, self).__init__()

    def get(self):
        return {'stuff': 'a value'}

    def post(self):
        pass


class LeagueAPI(Resource):
    def get(self, league_id):
        pass

    def put(self, league_id):
        pass

    def delete(self, league_id):
        pass