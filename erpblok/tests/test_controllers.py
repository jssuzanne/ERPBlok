from anyblok_pyramid.tests.testcase import PyramidDBTestCase
from anyblok.config import Configuration


class TestControllers(PyramidDBTestCase):

    @classmethod
    def setUpClass(cls):
        import erpblok.client.homepage  # noqa
        import erpblok.client.login  # noqa
        super(TestControllers, cls).setUpClass()

    def test_1_get_homepage(self):
        self.init_registry(None)
        response = self.webserver.get('/')
        self.assertEqual(response.status, '302 Found')
        db_name = Configuration.get('db_name')
        location = 'http://localhost/login?database=%s' % db_name
        self.assertEqual(response.location, location)
