from anyblok_pyramid.tests.testcase import PyramidDBTestCase
from anyblok.config import Configuration


class TestControllers(PyramidDBTestCase):

    def test_1_get_homepage(self):
        self.init_registry(None)
        response = self.webserver.get('/')
        self.assertEqual(response.status, '302 Found')
        db_name = Configuration.get('db_name')
        login_location = 'http://localhost/login?database=%s' % db_name
        self.assertEqual(response.location, login_location)

    def test_log_in_logout(self):
        registry = self.init_registry(None)
        db_name = Configuration.get('db_name')
        registry.Web.Login.update_admin('login', 'password')
        response = self.webserver.post(
            '/login/connect', {'database': db_name,
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
        login_location = 'http://localhost/login?database=%s' % db_name
        self.assertEqual(response.location, login_location)

    def test_logo(self):
        self.init_registry(None)
        response = self.webserver.get('/login/logo')
        self.assertEqual(response.status, '302 Found')
        self.assertEqual(response.location,
                         'http://localhost/static/login-logo.png')

    def test_get_db_manager(self):
        self.init_registry(None)
        response = self.webserver.get('/login/databases')
        self.assertEqual(response.status, '200 OK')
