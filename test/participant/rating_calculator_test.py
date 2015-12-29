from app.participant.models import create_participant
from app.participant.rating_calculator import RatingCalculator
from cases import BaseFlaskTestCase


class RatingCalculatorTests(BaseFlaskTestCase):
    def setUp(self):
        super(RatingCalculatorTests, self).setUp()
        self.create_test_participant()
        self.opponent = create_participant(self.user, self.league.league_id, 'Uni')

    def test_returned_participants_are_same(self):
        returned_participant, returned_opponent = \
            RatingCalculator(self.league, self.participant, self.opponent, winner=self.participant).process()

        self.assertEqual(self.participant, returned_participant)
        self.assertEqual(self.opponent, returned_opponent)

    def test_rating_calculator_updates_games_played_by_1(self):
        RatingCalculator(self.league, self.participant, self.opponent, winner=self.participant).process()

        self.assertEquals(self.participant.games_played, 1)
        self.assertEquals(self.opponent.games_played, 1)

    def test_returned_ratings_are_updated(self):
        RatingCalculator(self.league, self.participant, self.opponent, winner=self.participant).process()

        self.assertEquals(self.participant.rating, 1410.0)
        self.assertEquals(self.opponent.rating, 1390.0)

    def test_playing_k_factor_scaling_games_reduces_k_factor_to_min(self):
        for x in xrange(0, int(self.league.k_factor_scaling)):
                RatingCalculator(self.league, self.participant, self.opponent, winner=self.participant).process()

        self.assertEquals(self.participant.k_factor, self.league.k_factor_min)
        self.assertEquals(self.opponent.k_factor, self.league.k_factor_min)
