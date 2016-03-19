from anyblok_pyramid.tests.testcase import PyramidDBTestCase
from anyblok.config import Configuration
from anyblok import Declarations
import erpblok.client.homepage  # noqa


class TestHomepage(PyramidDBTestCase):

    @classmethod
    def setUpClass(cls):
        super(TestHomepage, cls).setUpClass()
        print(Declarations.Pyramid.routes)
        print(Declarations.Pyramid.views)

    def test_1_get_homepage(self):
        self.init_registry(None)
        response = self.webserver.get('/')
        self.assertEqual(response.status, '302 Found')
        db_name = Configuration.get('db_name')
        location = 'http://localhost/login?database=%s' % db_name
        self.assertEqual(response.location, location)
