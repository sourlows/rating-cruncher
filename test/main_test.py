from cases import BaseFlaskTestCase


class IndexTests(BaseFlaskTestCase):
    def test_returns_200(self):
        result = self.app.get('/')
        self.assertEqual(200, result.status_code)


class PageNotFoundTests(BaseFlaskTestCase):
    def test_returns_404(self):
        # There shouldn't be an /omgcats path, so this should return 404 (until an /omgcats directory is added)
        result = self.app.get('/omgcats')
        self.assertEquals(404, result.status_code)