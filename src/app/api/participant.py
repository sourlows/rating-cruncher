from flask_restful import marshal, fields
from app.api.base import BaseAuthResource
from app.league.models import LeagueModel
from app.participant.models import ParticipantModel, create_participant, delete_participant
from app.participant.rating_calculator import RatingCalculator

PARTICIPANT_TEMPLATE = {
    'league_id': fields.String,
    'participant_id': fields.String,
    'name': fields.String,
    'rating': fields.Float
}


class ParticipantListAPI(BaseAuthResource):
    OPTIONAL_ARGS = ['name', 'rating']

    def get(self, league_id):
        participants = ParticipantModel.query(getattr(ParticipantModel, 'league_id') == league_id).fetch()
        return [marshal(participant, PARTICIPANT_TEMPLATE) for participant in participants]

    def post(self, league_id):
        new_participant = create_participant(self.user, league_id, self.args.get('name'),
                                             rating=float(self.args.get('rating')))
        return marshal(new_participant, PARTICIPANT_TEMPLATE)


class ParticipantAPI(BaseAuthResource):
    OPTIONAL_ARGS = ['name', 'rating', 'opponent_id', 'winner']

    def get(self, league_id, participant_id):
        # pylint: disable=W0612,W0613
        participant = ParticipantModel.build_key(participant_id).get()
        if not participant:
            return 'Participant not found for %s' % participant_id, 404
        return marshal(participant, PARTICIPANT_TEMPLATE)

    def put(self, league_id, participant_id):
        participant = ParticipantModel.build_key(participant_id).get()
        opponent = ParticipantModel.build_key(self.args.get('opponent_id')).get()
        if not participant or not opponent:
            return 'Invalid participant id', 404
        league = LeagueModel.build_key(league_id, self.user.key).get()
        winner = ParticipantModel.build_key(self.args.get('winner')).get() if self.args.get('winner') else None
        participant, opponent = RatingCalculator(league, participant, opponent, winner).process()
        return marshal(participant, PARTICIPANT_TEMPLATE)

    def delete(self, league_id, participant_id):
        # pylint: disable=W0612,W0613
        try:
            delete_participant(self.user, participant_id)
        except ValueError:
            return 'Invalid participant id %s' % participant_id, 404
        return {'data': 'Success'}
