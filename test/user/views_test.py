from google.appengine.api import users

from app.user.models import create_user
from app.user.views import get_authed_user
from cases import BaseFlaskTestCase


class GetAuthedUserTests(BaseFlaskTestCase):
    def test_not_session_user_returns_none(self):
        self.assertIsNone(get_authed_user())

    def test_not_existing_user(self):
        user = users.User("Nep.Nep@planeptune.com", _user_id='nepnep')
        self.mock_function_in_setup('app.user.views.users.get_current_user', return_value=user)
        authed_user = get_authed_user()
        self.assertEqual(authed_user.user_id, 'nepnep')

    def test_existing_user(self):
        user = users.User("Nep.Nep@planeptune.com", _user_id='nepnep')
        self.mock_function_in_setup('app.user.views.users.get_current_user', return_value=user)
        create_user(user.user_id(), 'Neptune', 'Planeptune')
        authed_user = get_authed_user()
        self.assertEqual(authed_user.user_id, 'nepnep')
        self.assertEqual(authed_user.name, 'Neptune')
        self.assertEqual(authed_user.company_name, 'Planeptune')