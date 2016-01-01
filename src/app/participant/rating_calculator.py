class RatingCalculator(object):
    def __init__(self, league, participant, opponent, winner=None):
        self.participant = participant
        self.opponent = opponent
        self.winner = winner if winner else None
        self.league = league

    def process(self):
        expected_score_participant = 1.0 / (1.0 + pow(10.0, ((self.participant.rating - self.opponent.rating) / 400.0)))
        expected_score_opponent = 1.0 - expected_score_participant

        participant_is_winner = bool(self.participant == self.winner)
        if not self.winner:
            participant_score = 0.5
        elif participant_is_winner:
            participant_score = 1.0
        else:
            participant_score = 0.0
        opponent_score = 1.0 - participant_score

        self.participant.rating += self.participant.k_factor * (participant_score - expected_score_participant)
        self.opponent.rating += self.opponent.k_factor * (opponent_score - expected_score_opponent)

        self.participant.games_played += 1
        self.opponent.games_played += 1

        if self.league.k_factor_scaling != 0:
            k_factor_reduction = (self.league.k_factor_initial - self.league.k_factor_min) / \
                                                                   self.league.k_factor_scaling
            if self.participant.games_played <= self.league.k_factor_scaling:
                self.participant.k_factor -= k_factor_reduction
            if self.opponent.games_played <= self.league.k_factor_scaling:
                self.opponent.k_factor -= k_factor_reduction

        self.participant.put()
        self.opponent.put()

        return self.participant, self.opponent
