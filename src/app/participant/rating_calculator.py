class RatingCalculator:
    def __init__(self, participant, opponent, winner=None):
        self.participant = participant
        self.opponent = opponent
        self.winner = winner if winner else None

    def process(self):
        expected_score_participant = 1.0/(1.0 + pow(10.0, ((self.participant.rating - self.opponent.rating)/400.0)))
        expected_score_opponent = 1.0 - expected_score_participant

        participant_is_winner = bool(self.participant == self.winner)
        if not self.winner:
            participant_score = 0.5
        elif participant_is_winner:
            participant_score = 1.0
        else:
            participant_score = 0.0
        opponent_score = 1.0 - participant_score

        # temporary; will be replaced with participant's K value later
        k = 32.0

        self.participant.rating += k * (participant_score - expected_score_participant)
        self.opponent.rating += k * (opponent_score-expected_score_opponent)

        self.participant.put()
        self.opponent.put()

        return self.participant, self.opponent
