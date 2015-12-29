from app.participant.models import create_participant
from app.participant.rating_calculator import RatingCalculator
from cases import BaseFlaskTestCase


class RatingCalculatorTests(BaseFlaskTestCase):
    def test_returned_participants_are_same(self):
        self.create_test_participant()
        opponent = create_participant(self.user, self.league.league_id, 'Uni')

        returned_participant, returned_opponent = \
            RatingCalculator(self.league, self.participant, opponent, winner=self.participant).process()

        self.assertEqual(self.participant, returned_participant)
        self.assertEqual(opponent, returned_opponent)

    def test_rating_calculator_updates_games_played_by_1(self):
        self.create_test_participant()
        opponent = create_participant(self.user, self.league.league_id, 'Uni')

        RatingCalculator(self.league, self.participant, opponent, winner=self.participant).process()

        self.assertEquals(self.participant.games_played, 1)
        self.assertEquals(opponent.games_played, 1)

    def test_returned_ratings_are_updated(self):
        self.create_test_participant()
        opponent = create_participant(self.user, self.league.league_id, 'Uni')

        RatingCalculator(self.league, self.participant, opponent, winner=self.participant).process()

        self.assertEquals(self.participant.rating, 1410.0)
        self.assertEquals(opponent.rating, 1390.0)

    def test_playing_k_factor_scaling_games_reduces_k_factor_to_min(self):
        self.create_test_participant()
        opponent = create_participant(self.user, self.league.league_id, 'Uni')
        q = RatingCalculator(self.league, self.participant, opponent, winner=self.participant)
        for x in xrange(0, int(self.league.k_factor_scaling)):
            returned_participant, returned_opponent = q.process()

        self.assertEquals(returned_participant.k_factor, self.league.k_factor_min)
        self.assertEquals(returned_opponent.k_factor, self.league.k_factor_min)
