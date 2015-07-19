__author__ = 'Alex'


class RatingCalculator():
    def __init__(self, participant_q, participant_v, winner=None):
        self.participant_q = participant_q
        self.participant_v = participant_v
        self.winner = winner

    def process(self):
        expected_score_q = 1/(1 + pow(10, ((self.participant_q - self.participant_v)/400)))
        expected_score_v = 1/(1 + pow(10, ((self.participant_v - self.participant_q)/400)))
        K = 32
        if not self.winner:
            updated_q = self.participant_q + K*(0.5 - expected_score_q)
            updated_v = self.participant_v + K*(0.5 - expected_score_v)
        elif self.winner == self.participant_q:
            updated_q = self.participant_q + K*(1 - expected_score_q)
            updated_v = self.participant_v + K*(0 - expected_score_v)
        else:
            updated_q = self.participant_q + K*(0 - expected_score_q)
            updated_v = self.participant_v + K*(1 - expected_score_v)

        return updated_q, updated_v