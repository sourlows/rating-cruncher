__author__ = 'Alex'


class RatingCalculator():
    def __init__(self, participant_q, participant_v, winner=None):
        self.participant_q = participant_q
        self.participant_v = participant_v
        self.winner = winner

    def process(self):
        #Eq + Ev = 1
        expected_score_q = 1.0/(1.0 + pow(10.0, ((self.participant_q.rating - self.participant_v.rating)/400.0)))
        expected_score_v = 1.0 - expected_score_q

        # temporary; will be replaced with participant's K value later
        K = 32.0
        q_score = 1.0 if self.participant_q == self.winner else 0.0
        v_score = 1.0 - q_score

        self.participant_q.rating = self.participant_q + K * (q_score-expected_score_q)
        self.participant_v.rating = self.participant_v + K * (v_score-expected_score_v)

        self.participant_q.put()
        self.participant_v.put()

        return self.participant_q, self.participant_v