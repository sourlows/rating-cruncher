from app.api.base import BaseAuthResource
from app.league.models import LeagueModel
from app.participant.models import ParticipantModel, create_participant, delete_participant
from app.participant.rating_calculator import RatingCalculator
from flask.ext.restful import marshal, fields

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
        return [marshal(participant, participant_template) for participant in participants]

    def post(self, league_id):
        new_participant = create_participant(self.user, league_id, self.args.get('name'),
                                             rating=float(self.args.get('rating')))
        return marshal(new_participant, participant_template)


class ParticipantAPI(BaseAuthResource):
    OPTIONAL_ARGS = ['name', 'rating', 'opponent_id', 'winner']

    def get(self, league_id, participant_id):
        participant = ParticipantModel.build_key(participant_id).get()
        if not participant:
            return 'Participant not found for %s' % participant_id, 404
        return marshal(participant, participant_template)

    def put(self, league_id, participant_id):
        participant = ParticipantModel.build_key(participant_id).get()
        opponent = ParticipantModel.build_key(self.args.get('opponent_id')).get()
        if not participant or not opponent:
            return 'Invalid participant id', 404
        league = LeagueModel.build_key(league_id, self.user.key)
        winner = ParticipantModel.build_key(self.args.get('winner')).get() if self.args.get('winner') else None
        participant, opponent = RatingCalculator(league, participant, opponent, winner).process()
        return marshal(participant, participant_template)

    def delete(self, league_id, participant_id):
        try:
            delete_participant(self.user, participant_id)
        except ValueError:
            return 'Invalid participant id %s' % participant_id, 404
        return {'data': 'Success'}