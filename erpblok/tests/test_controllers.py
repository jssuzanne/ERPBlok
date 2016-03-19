from anyblok_pyramid.tests.testcase import PyramidDBTestCase
from anyblok.config import Configuration


class TestControllers(PyramidDBTestCase):

    @classmethod
    def setUpClass(cls):
        import erpblok.client.homepage  # noqa
        import erpblok.client.login  # noqa
        import erpblok.client.web  # noqa
        super(TestControllers, cls).setUpClass()

    def test_1_get_homepage(self):
        registry = self.init_registry(None)
        response = self.webserver.get('/')
        self.assertEqual(response.status, '302 Found')
        db_name = Configuration.get('db_name')
        login_location = 'http://localhost/login?database=%s' % db_name
        self.assertEqual(response.location, login_location)
        registry.Web.Login.update_admin('login', 'password')
        response = self.webserver.post('/login/connect', {'database': db_name,
                                                          'login': 'login',
                                                          'password': 'password'})
        self.assertEqual(response.status, '200 OK')
        response = self.webserver.get('/')
        self.assertEqual(response.status, '302 Found')
        app_location = 'http://localhost/web/client'
        self.assertEqual(response.location, app_location)
        response = self.webserver.get('/login', {'database': db_name})
        self.assertEqual(response.status, '200 OK')
        response = self.webserver.post('/login/disconnect', {})
        self.assertEqual(response.status, '200 OK')
        response = self.webserver.get('/')
        self.assertEqual(response.status, '302 Found')
        self.assertEqual(response.location, login_location)
        response = self.webserver.get('/login/logo')
        self.assertEqual(response.status, '302 Found')
        response = self.webserver.get('/login/databases')
        self.assertEqual(response.status, '200 OK')
