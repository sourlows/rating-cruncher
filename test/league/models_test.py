from app.league.models import LeagueModel, create_league, update_league, delete_league
from app.user.models import create_user
from cases import BaseFlaskTestCase


class LeagueModelTests(BaseFlaskTestCase):
    def test_generate_id(self):
        league_id = LeagueModel.generate_id()
        self.assertTrue('LG-' in league_id)

    def test_build_key(self):
        # TODO
        pass

    def test_update_participant_count(self):
        q = LeagueModel(league_id=LeagueModel.generate_id(), rating_scheme='ELO')
        self.assertEquals(q.participant_count, 0)
        q.update_participant_count(3)
        self.assertEquals(q.participant_count, 3)


class CreateLeagueTests(BaseFlaskTestCase):
    def test_create_league(self):
        self.create_test_league()
        self.assertEqual(self.league.name, 'Nep League')
        self.assertTrue('LG-' in self.league.league_id)
        self.assertEqual(self.league.rating_scheme, 'ELO')


class UpdateLeagueTests(BaseFlaskTestCase):
    def test_raise_if_league_id_is_none(self):
        with self.assertRaises(ValueError):
            update_league(create_user('Name'), league_id=None, name='League', rating_scheme='ELO')

    def test_raise_if_invalid_league_id(self):
        with self.assertRaises(ValueError):
            update_league(create_user('Name'), league_id='Not A League ID', name='League', rating_scheme='ELO')

    def test_update_league(self):
        self.create_test_league()
        self.assertEqual(self.league.name, 'Nep League')
        self.assertTrue('LG-' in self.league.league_id)
        self.assertEqual(self.league.rating_scheme, 'ELO')
        update_league(self.user, self.league.league_id, name='Lastation League', rating_scheme='type1')
        self.assertEqual(self.league.name, 'Lastation League')
        self.assertEqual(self.league.rating_scheme, 'type1')


class DeleteLeagueTests(BaseFlaskTestCase):
    def test_delete_league(self):
        self.create_test_league()
        delete_league(user=self.user, league_id=self.league.league_id)
        key = LeagueModel.build_key(self.league.league_id, self.user.key)
        league = key.get()
        self.assertIsNone(league)