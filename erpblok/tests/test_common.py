from anyblok.tests.testcase import DBTestCase
from anyblok.config import Configuration
from erpblok.client import common


class MockSession(dict):

    def __init__(self, *args, **kwargs):
        super(MockSession, self).__init__(*args, **kwargs)
        self.is_saved = False

    def save(self):
        self.is_saved = True


class MockRequest:

    session = MockSession()


class TestCommon(DBTestCase):

    def test_list_databases(self):
        self.init_registry(None)
        db_name = Configuration.get('db_name')
        self.assertIn(db_name, common.list_databases())

    def test_create_and_drop_databases(self):
        db_name = Configuration.get('db_name') + '_test'
        self.assertNotIn(db_name, common.list_databases())
        registry = common.create_database(db_name)
        self.assertIsNotNone(registry)
        self.assertIn(db_name, common.list_databases())
        common.drop_database(db_name)
        self.assertNotIn(db_name, common.list_databases())

    def test_login_and_logout(self):
        request = MockRequest()
        user_id = 1
        self.assertTrue(common.login_user(
            request, 'database', 'login', 'password', user_id))
        self.assertEqual(request.session['database'], 'database')
        self.assertEqual(request.session['login'], 'login')
        self.assertEqual(request.session['password'], 'password')
        self.assertEqual(request.session['user_id'], user_id)
        self.assertEqual(request.session['state'], 'connected')
        self.assertTrue(common.logout(request))
        self.assertEqual(request.session['database'], 'database')
        self.assertEqual(request.session['login'], '')
        self.assertEqual(request.session['password'], '')
        self.assertEqual(request.session['user_id'], '')
        self.assertEqual(request.session['state'], 'disconnected')

    def test_format_static(self):
        self.assertEqual(
            common.format_static('myblok', '/one/url'), '/one/url')
        self.assertEqual(
            common.format_static('myblok', '#BLOK/one/url'), '/myblok/one/url')

    def test_get_static(self):
        self.assertFalse(common.get_static('unknown_entries'))
        self.assertTrue(common.get_static('global_js'))

    def test_get_templates_from(self):
        self.assertFalse(common.get_templates_from('unknown_template'))
        self.assertTrue(common.get_templates_from('login_templates'))
