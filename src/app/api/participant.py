from app.RatingCalculator import RatingCalculator
from app.api.base import BaseAuthResource
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
    def get(self):
        participants = ParticipantModel.query(league_id=self.args.league_id).fetch()
        return {'data': [marshal(participant, participant_template) for participant in participants]}

    def post(self):
        new_participant = create_participant(self.user.user_id, self.args.get('league_id'),
                                             self.args.get('name'), rating=self.args.get('rating'))
        return {'data': marshal(new_participant, participant_template)}


class ParticipantAPI(BaseAuthResource):
    OPTIONAL_ARGS = ['name', 'rating']

    def get(self):
        participant = ParticipantModel.build_key(participant_id=self.args.participant_id).get()
        return {'data': marshal(participant, participant_template)}

    def put(self, opponent_id, winner=None):
        r, q = RatingCalculator(self.args.participant_id, opponent_id, winner=winner).process()

        return{'data': marshal(r, participant_template)}

    def delete(self):
        delete_participant(self.args.participant_id)
        return {'data': 'Success'}