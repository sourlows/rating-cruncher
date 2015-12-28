from app.participant.models import create_participant
from app.participant.rating_calculator import RatingCalculator
from cases import BaseFlaskTestCase


class RatingCalculatorTest(BaseFlaskTestCase):
    def test(self):
        self.create_test_participant()
        opponent = create_participant(self.user, self.league.league_id, 'Uni')
        q = RatingCalculator(self.league, self.participant, opponent, winner=self.participant)
        returned_participant, returned_opponent = q.process()

        self.assertEqual(self.participant, returned_participant)
        self.assertEqual(opponent, returned_opponent)

        self.assertEquals(self.participant.games_played, 1)
        self.assertEquals(opponent.games_played, 1)

        self.assertEquals(self.participant.rating, 1410.0)
        self.assertEquals(opponent.rating, 1390.0)

        for x in xrange(0, int(self.league.k_factor_scaling)):
            returned_participant, returned_opponent = q.process()

        self.assertEquals(returned_participant.k_factor, self.league.k_factor_min)
        self.assertEquals(returned_opponent.k_factor, self.league.k_factor_min)
