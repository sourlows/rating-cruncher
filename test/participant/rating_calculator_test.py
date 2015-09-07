from app.participant.models import create_participant
from app.participant.rating_calculator import RatingCalculator
from cases import BaseFlaskTestCase


class RatingCalculatorTest(BaseFlaskTestCase):
    def test(self):
        self.create_test_participant()
        opponent = create_participant(self.user, self.league.league_id, 'Uni')
        q = RatingCalculator(self.participant, opponent, winner=self.participant)
        returned_participant, returned_opponent = q.process()
        self.assertEqual(self.participant, returned_participant)
        self.assertEqual(opponent, returned_opponent)