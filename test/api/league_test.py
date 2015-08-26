import json
from app.league.models import create_league
from app.user.models import create_user
from cases import BaseFlaskTestCase


class LeagueListAPITests(BaseFlaskTestCase):
    def setUp(self):
        super(LeagueListAPITests, self).setUp()
        self.auth_mock = self.mock_function_in_setup('app.api.base.api_auth.authenticate', return_value=True)
        self.args_mock = self.mock_function_in_setup('app.api.base.reqparse.RequestParser.parse_args',
                                                     return_value={'username': 'nepnep'})
        self.create_test_user()

    def test_get_returns_all_leagues_associated_to_user(self):
        league_n = create_league(self.user, name="Nep League", rating_scheme='ELO')
        league_m = create_league(self.user, name="Noire League", rating_scheme='type1')

        data = json.loads(self.app.get('/api/league/').data)

        expected_n = {
            'league_id': league_n.league_id,
            'rating_scheme': league_n.rating_scheme,
            'name': league_n.name,
            'description': league_n.description,
            'participant_count': league_n.participant_count
        }
        expected_m = {
            'league_id': league_m.league_id,
            'rating_scheme': league_m.rating_scheme,
            'name': league_m.name,
            'description': league_m.description,
            'participant_count': league_m.participant_count
        }

        self.assertTrue(expected_n in data and
                        expected_m in data)

    def test_get_does_not_return_leagues_not_associated_to_user(self):
        self.create_test_user()
        different_user = create_user('gege', name='Nepgear', company_name='Planeptune')

        league_n = create_league(different_user, name="Nep League", rating_scheme='ELO')
        league_m = create_league(different_user, name="Noire League", rating_scheme='ELO')

        data = json.loads(self.app.get('/api/league/').data)

        expected_n = {
            'league_id': league_n.league_id,
            'rating_scheme': league_n.rating_scheme,
            'name': league_n.name,
            'description': league_n.description,
            'participant_count': league_n.participant_count
        }
        expected_m = {
            'league_id': league_m.league_id,
            'rating_scheme': league_m.rating_scheme,
            'name': league_m.name,
            'description': league_m.description,
            'participant_count': league_m.participant_count
        }
        self.assertFalse(expected_n in data or
                         expected_m in data)

    def test_get_returns_empty_list_if_no_leagues_are_associated_to_user(self):
        response = self.app.get('/api/league/')
        self.assertEqual(json.loads(response.data), [])

    def test_post_returns_400_if_invalid_rating_scheme_is_specified(self):
        self.args_mock.return_value = {
            'username': 'nepnep',
            'rating_scheme': 'wrong',
        }
        response = self.app.post('/api/league/')
        self.assertEqual(response.status_code, 400)

    def test_post_new_league_when_created_successfully(self):
        self.args_mock.return_value = {
            'username': 'nepnep',
            'rating_scheme': 'type1',
        }
        response = self.app.post('/api/league/')
        self.assertEqual(response.status_code, 200)


class LeagueAPITests(BaseFlaskTestCase):
    def setUp(self):
        super(LeagueAPITests, self).setUp()
        self.auth_mock = self.mock_function_in_setup('app.api.base.api_auth.authenticate', return_value=True)
        self.args_mock = self.mock_function_in_setup('app.api.base.reqparse.RequestParser.parse_args',
                                                     return_value={'username': 'nepnep'})
        self.create_test_user()

    def test_get_returns_404_if_missing_league_id_is_specified(self):
        response = self.app.get('/api/league/Not A League ID')
        self.assertEqual(response.status_code, 404)

    def test_get_returns_league_for_specified_league_id(self):
        self.create_test_league()
        expected_l = {            
            'league_id': self.league.league_id,
            'rating_scheme': self.league.rating_scheme,
            'name': self.league.name,
            'description': self.league.description,
            'participant_count': self.league.participant_count            
        }
        self.assertEqual(json.loads(self.app.get('api/league/'+self.league.league_id).data), expected_l)

    def test_put_returns_404_if_missing_league_id_is_specified(self):
        response = self.app.put('/api/league/Not A League ID')
        self.assertEqual(response.status_code, 404)

    def test_put_returns_400_if_invalid_elo_scheme_is_specified(self):
        self.create_test_league()
        self.args_mock.return_value = {
            'username': 'nepnep',
            'rating_scheme': 'Not A Rating Scheme',
        }
        response = self.app.put('/api/league/'+self.league.league_id)
        self.assertEqual(response.status_code, 400)

    def test_put_returns_updated_league(self):
        self.create_test_league()
        self.args_mock.return_value = {
            'username': 'nepnep',
            'name': 'nep',
            'rating_scheme': 'type2',
            'description': 'aaaaa',
            'participant_count': 0,
        }
        response = self.app.put('/api/league/'+self.league.league_id)
        data = json.loads(response.data)
        expected_m = {
            u'league_id': self.league.league_id,
            u'rating_scheme': u'type2',
            u'name': u'nep',
            u'description': u'aaaaa',
            u'participant_count': 0,
        }
        self.assertEqual(expected_m, data)

    def test_delete_returns_404_if_missing_league_id_is_specified(self):
        self.assertEqual(self.app.delete('/api/league/Not A League ID').status_code, 404)

    def test_delete_returns_200_if_specified_league_is_deleted(self):
        self.create_test_league()
        self.assertEqual(self.app.delete('/api/league/'+self.league.league_id).status_code, 200)