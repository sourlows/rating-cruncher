from app.user.models import create_user, UserModel, update_user
from cases import BaseFlaskTestCase


class CreateUserTests(BaseFlaskTestCase):
    def test_raises_if_user_id_is_none(self):
        with self.assertRaises(ValueError):
            create_user(user_id=None)

    def test_create_user(self):
        user = create_user('abc', name='Nepgear', company_name='Planeptune')
        self.assertEqual(user.user_id, 'abc')
        self.assertEqual(user.name, 'Nepgear')
        self.assertEqual(user.company_name, 'Planeptune')


class UpdateUserTests(BaseFlaskTestCase):
    def test_not_user_id(self):
        with self.assertRaises(ValueError):
            create_user(user_id=None)

    def test_update_user(self):
        create_user('abc', name='name1', company_name='company name1')
        update_user('abc', name='name2', company_name='company_name2')
        user = UserModel.build_key(user_id='abc').get()
        self.assertEqual(user.user_id, 'abc')
        self.assertEqual(user.name, 'name2')
        self.assertEqual(user.company_name, 'company_name2')

    def test_raise_if_user_id_is_none(self):
        with self.assertRaises(ValueError):
            update_user(user_id=None)

    def test_raise_if_not_existing_user(self):
        with self.assertRaises(ValueError):
            update_user(user_id="NotAUser")