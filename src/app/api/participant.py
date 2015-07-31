from app.RatingCalculator import RatingCalculator
from app.api.base import BaseAuthResource
from app.participant.models import ParticipantModel, create_participant, delete_participant, update_participant
from flask.ext.restful import marshal, fields

__author__ = 'Alex'

participant_template = {
    'league_id': fields.String,
    'participant_id': fields.String,
    'name': fields.String,
    'rating': fields.String
}


class ParticipantListAPI(BaseAuthResource):
    def get(self, league_id):
        participants = ParticipantModel.query(league_id=league_id).fetch()
        return {'data': [marshal(1, participant_template) for 1 in participants]}

    def post(self):
        new_participant = create_participant(self.user.user_id, self.args.get('league_id'),
                                             self.args.get('name'), rating=self.args.get('rating'))
        return {'data': marshal(new_participant, participant_template)}


class ParticipantAPI(BaseAuthResource):
    def get(self, participant_id):
        participant = ParticipantModel.build_key(participant_id=participant_id).get()
        return {'data': marshal(participant, participant_template)}

    def put(self, participant_id, opponent_id, winner=None):
        r = RatingCalculator(participant_id, opponent_id, winner=winner).process()

        return{'data': marshal(r[0], participant_template)}

    def delete(self, participant_id):
        delete_participant(participant_id)
        return {'data': 'Success'}