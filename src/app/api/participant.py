from app.RatingCalculator import RatingCalculator
from app.api.base import BaseAuthResource
from app.league.models import LeagueModel
from app.participant.models import ParticipantModel, create_participant, delete_participant, update_participant
from flask.ext.restful import marshal, fields

__author__ = 'Alex'

participant_template = {
    'league_id': fields.String,
    'participant_id': fields.String,
    'name': fields.String,
    'rating': fields.Float
}


class ParticipantListAPI(BaseAuthResource):
    OPTIONAL_ARGS = ['name', 'rating']

    def get(self, league_id):
        participants = ParticipantModel.query(getattr(ParticipantModel, 'league_id') == league_id).fetch()
        return {'data': [marshal(participant, participant_template) for participant in participants]}

    def post(self, league_id):
        new_participant = create_participant(self.user, league_id, self.args.get('name'),
                                             rating=float(self.args.get('rating')))
        return {'data': marshal(new_participant, participant_template)}


class ParticipantAPI(BaseAuthResource):
    OPTIONAL_ARGS = ['name', 'rating']

    def get(self, league_id, participant_id):
        participant = ParticipantModel.build_key(participant_id).get()
        return {'data': marshal(participant, participant_template)}

    def put(self, league_id, participant_id, opponent_id, winner=None):
        q, r = RatingCalculator(participant_id, opponent_id, winner)
        return{'data': marshal(q, participant_template)}

    def delete(self, league_id, participant_id):
        delete_participant(self.user, participant_id)
        return {'data': 'Success'}
