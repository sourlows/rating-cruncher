import json
from cases import BaseFlaskTestCase


class LeagueListAPITests(BaseFlaskTestCase):
    def setUp(self):
        super(LeagueListAPITests, self).setUp()
        self.auth_mock = self.mock_function_in_setup('app.api.base.api_auth.authenticate', return_value=True)
        self.args_mock = self.mock_function_in_setup('app.api.base.reqparse.RequestParser.parse_args',
                                                     return_value={'username': 'nepnep'})
        self.create_test_user()

    def test_get_returns_all_leagues_associated_to_user(self):
        pass

    def test_get_does_not_return_leagues_not_associated_to_user(self):
        pass

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
        pass


class LeagueAPITests(BaseFlaskTestCase):
    def test_get_returns_400_if_no_league_id_is_specified(self):
        pass

    def test_get_returns_404_if_missing_league_id_is_specified(self):
        pass

    def test_get_returns_league_for_specified_league_id(self):
        pass

    def test_put_returns_400_if_no_league_id_is_specified(self):
        pass

    def test_put_returns_404_if_missing_league_id_is_specified(self):
        pass

    def test_put_returns_400_if_invalid_elo_scheme_is_specified(self):
        pass

    def test_put_returns_updated_league(self):
        pass

    def test_delete_returns_400_if_no_league_id_is_specified(self):
        pass

    def test_delete_returns_404_if_missing_league_id_is_specified(self):
        pass

    def test_delete_returns_200_if_specified_league_is_deleted(self):
        pass