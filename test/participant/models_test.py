from app.participant.models import ParticipantModel, update_participant, delete_participant
from cases import BaseFlaskTestCase


class ParticipantModelTests(BaseFlaskTestCase):
    def test_generate_id(self):
        participant_id = ParticipantModel.generate_id()
        self.assertTrue('P-' in participant_id)


class CreateParticipantTests(BaseFlaskTestCase):
    def test_create_participant(self):
        self.create_test_participant()
        self.assertEqual(self.participant.name, 'Nepgear')
        self.assertEqual(self.participant.rating, 1400.0)


class UpdateParticipantTests(BaseFlaskTestCase):
    def test_update_participant(self):
        self.create_test_participant()
        self.assertEqual(self.participant.name, 'Nepgear')
        self.assertEqual(self.participant.rating, 1400.0)
        update_participant(self.participant.participant_id, 'Noire', 1200.0)
        self.assertEqual(self.participant.name, 'Noire')
        self.assertEqual(self.participant.rating, 1200.0)

    def test_raises_if_not_participant_id(self):
        with self.assertRaises(ValueError):
            self.create_test_participant()
            update_participant(None, self.participant.name, self.participant.rating)

    def test_raises_if_not_participant(self):
        with self.assertRaises(ValueError):
            self.create_test_league()
            update_participant(ParticipantModel.generate_id(), 'Name', 1400.0)


class DeleteParticipantTests(BaseFlaskTestCase):
    def test_delete_participant(self):
        self.create_test_participant()
        delete_participant(self.user, self.participant.participant_id)
        key = ParticipantModel.build_key(self.participant.participant_id)
        participant = key.get()
        self.assertIsNone(participant)