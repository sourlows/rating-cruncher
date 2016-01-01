from app.user.models import create_user, update_user
from cases import BaseFlaskTestCase


class CreateUserTests(BaseFlaskTestCase):
    def test_raises_if_user_id_is_none(self):
        with self.assertRaises(ValueError):
            create_user(user_id=None)

    def test_create_user(self):
        self.create_test_user()
        self.assertEqual(self.user.user_id, 'nepnep')
        self.assertEqual(self.user.name, 'Neptune')
        self.assertEqual(self.user.company_name, 'Planeptune')


class UpdateUserTests(BaseFlaskTestCase):
    def test_update_user(self):
        self.create_test_user()
        update_user(self.user.user_id, name='Nepgear', company_name='company_name2')
        self.assertEqual(self.user.user_id, 'nepnep')
        self.assertEqual(self.user.name, 'Nepgear')
        self.assertEqual(self.user.company_name, 'company_name2')

    def test_raise_if_user_id_is_none(self):
        with self.assertRaises(ValueError):
            update_user(user_id=None)

    def test_raise_if_not_existing_user(self):
        with self.assertRaises(ValueError):
            update_user(user_id="NotAUser")
