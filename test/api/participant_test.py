from app.league.models import create_league
from app.participant.models import create_participant
from app.user.models import create_user
from cases import BaseFlaskTestCase
import json


class ParticipantListAPITests(BaseFlaskTestCase):
    def setUp(self):
        super(ParticipantListAPITests, self).setUp()
        self.auth_mock = self.mock_function_in_setup('app.api.base.api_auth.authenticate', return_value=True)
        self.args_mock = self.mock_function_in_setup('app.api.base.reqparse.RequestParser.parse_args',
                                                     return_value={'username': 'nepnep'})
        self.create_test_user()

    def test_get_returns_all_participants_in_league(self):
        self.create_test_participant()
        participant = create_participant(user=self.user, league_id=self.league.league_id, name='Neptune', rating=1200.0)

        returned_participants_list = json.loads(self.app.get('/api/participant/' + self.league.league_id).data)

        expected_participant_0 = {
            'league_id': self.league.league_id,
            'rating': self.participant.rating,
            'name': self.participant.name,
            'participant_id': self.participant.participant_id,
        }
        expected_participant_1 = {
            'league_id': self.league.league_id,
            'rating': participant.rating,
            'name': participant.name,
            'participant_id': participant.participant_id,
        }

        self.assertTrue(expected_participant_0 in returned_participants_list and
                        expected_participant_1 in returned_participants_list)

    def test_get_does_not_return_participants_not_in_league(self):
        self.create_test_participant()
        different_league = create_league(self.user, 'New League', 'type2')
        participant = create_participant(user=self.user, league_id=different_league.league_id,
                                         name='Vert', rating=2200.0)

        returned_participants_list = json.loads(self.app.get('/api/participant/%s' % self.league.league_id).data)

        expected_participant = {
            'league_id': self.league.league_id,
            'rating': self.participant.rating,
            'name': self.participant.name,
            'participant_id': self.participant.participant_id,
        }
        unexpected_participant = {
            'league_id': different_league.league_id,
            'rating': participant.rating,
            'name': participant.name,
            'participant_id': participant.participant_id,
        }

        self.assertTrue(expected_participant in returned_participants_list and
                        not (unexpected_participant in returned_participants_list))

    def test_get_returns_empty_list_if_league_has_no_participants(self):
        self.create_test_league()
        self.assertEqual(json.loads(self.app.get('/api/participant/%s' % self.league.league_id).data), [])

    def test_post_new_participant_when_created_successfully(self):
        self.create_test_league()
        self.args_mock.return_value = {
            'username': 'nepnep',
            'league_id': self.league.league_id,
            'name': 'uni',
            'rating': 500,
        }
        self.assertEqual(self.app.post('/api/participant/' + self.league.league_id).status_code, 200)


class ParticipantAPITests(BaseFlaskTestCase):
    def setUp(self):
        super(ParticipantAPITests, self).setUp()
        self.auth_mock = self.mock_function_in_setup('app.api.base.api_auth.authenticate', return_value=True)
        self.args_mock = self.mock_function_in_setup('app.api.base.reqparse.RequestParser.parse_args',
                                                     return_value={'username': 'nepnep'})
        self.create_test_league()

    def test_get_returns_404_if_invalid_partcipant_id(self):
        response = self.app.get('/api/participant/%s/%s' % (self.league.league_id, 'InvalidParticipant')).status_code
        self.assertEqual(response, 404)

    def test_get_returns_participant_for_participant_id(self):
        self.create_test_participant()
        returned_participant = json.loads(
            self.app.get('/api/participant/%s/%s' % (self.league.league_id, self.participant.participant_id)).data)
        expected_participant = {
            u'league_id': self.league.league_id,
            u'participant_id': self.participant.participant_id,
            u'rating': self.participant.rating,
            u'name': self.participant.name,
        }
        self.assertEqual(returned_participant, expected_participant)

    def test_put_returns_404_if_invalid_participant_id(self):
        self.args_mock.return_value = {
            'username': 'nepnep',
            'opponent_id': 'InvalidID',
            'winner': None,
        }
        response = self.app.put('/api/participant/%s/%s' % (self.league.league_id, 'InvalidParticipant'))
        self.assertEqual(response.status_code, 404)

    def test_put_returns_updated_participant(self):
        self.create_test_participant()
        opponent = create_participant(self.user, self.league.league_id, 'Nepgear', 1400.0)
        self.args_mock.return_value = {
            'username': 'nepnep',
            'opponent_id': opponent.participant_id,
            'winner': self.participant.participant_id,
        }
        response = self.app.put('/api/participant/%s/%s' % (self.league.league_id, self.participant.participant_id))
        returned_participant = json.loads(response.data)
        expected_participant = {
            'participant_id': self.participant.participant_id,
            'league_id': self.league.league_id,
            'rating': self.participant.rating,
            'name': self.participant.name,
        }
        self.assertEqual(expected_participant, returned_participant)

    def test_delete_returns_404_if_invalid_participant_id(self):
        self.assertEqual(
            self.app.delete('/api/participant/%s/%s' % (self.league.league_id, 'NotAParticipant')).status_code, 404)

    def test_delete_returns_200_if_participant_is_deleted(self):
        self.create_test_participant()
        response = self.app.delete('/api/participant/%s/%s' % (self.league.league_id, self.participant.participant_id))
        self.assertEqual(response.status_code, 200)
