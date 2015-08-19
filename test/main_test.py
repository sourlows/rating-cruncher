__author__ = 'Alex'
from cases import BaseFlaskTestCase


class IndexTests(BaseFlaskTestCase):
    def test_returns_200(self):
        result = self.app.get('/')
        self.assertEqual(200, result.status_code)