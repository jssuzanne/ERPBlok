from anyblok import Declarations
from anyblok.config import Configuration
from anyblok.registry import RegistryManager
from .common import (list_databases, login_user, logout, get_static,
                     get_templates_from)
from pyramid.httpexceptions import HTTPUnauthorized, HTTPFound
from pyramid.response import Response


Declarations.Pyramid.add_route('login', '/login')
Declarations.Pyramid.add_route('login-logo', '/login/logo')
Declarations.Pyramid.add_route('login-databases', '/login/databases')
Declarations.Pyramid.add_route('login-connect', '/login/connect',
                               request_method='POST')
Declarations.Pyramid.add_route('login-disconnect', '/login/disconnect',
                               request_method='POST')


@Declarations.Pyramid.add_view('login', renderer='erpblok:client.mak')
def get_login(request, database=None):
    """ Display the login page

    """
    title = Configuration.get('app_name', 'ERPBlok')
    return {
        'title': title,
        'css': get_static('global_css') + get_static('login_css'),
        'js': get_static('global_js') + get_static('login_js'),
        'js_babel': (get_static('global_js_babel') +
                     get_static('login_js_babel')),
        'templates': get_templates_from('login_templates'),
    }


@Declarations.Pyramid.add_view('login-logo')
def get_login_logo(request):
    """ Return the logo for thelogin page """
    url_login_logo = Configuration.get('url_login_logo')
    if url_login_logo:
        return HTTPFound(location=url_login_logo)

    return HTTPFound(location="/static/login-logo.png")


@Declarations.Pyramid.add_view('login-databases', request_method="GET",
                               renderer="json")
def get_databases(request):
    res = [
        {
            'label': 'Databases',
            'icon': 'fi-database large',
            'menus': [{'id': x, 'label': x} for x in list_databases()],
        },
    ]
    if Configuration.get('allow_database_manager'):
        res.append({
            'label': 'Tools',
            'icon': 'fi-widget',
            'menus': [{'id': 'manage_db',
                       'label': 'Manage databases',
                       'icon': 'fi-wrench',
                       'description': "Create new or drop exising ERPBlok "
                                      "database. You may also insall or "
                                      "uninstall some low level management "
                                      "bloks"}],
        })

    return res


@Declarations.Pyramid.add_view('login-connect')
def post_login_connect(request, database=None, login=None, password=None):
    """ Log the user, if the login and password are right

    :param database: the target database
    :param login: the login to verify
    :param password: the password to verify
    :rtype: redirection if login/password is right else HTTPUnauthorized
    """
    registry = RegistryManager.get(database)
    user_id = registry.Web.Login.check_authentification(login, password)
    if user_id:
        if login_user(request, database, login, password, user_id):
            return Response(request.route_url('web-client'))

    return HTTPUnauthorized()


@Declarations.Pyramid.add_view('login-disconnect')
def post_login_disconnect(request, database=None):
    """ Logout the current user and do a redirect to the login page """
    logout(request)
    database = request.session.get('database')
    query = {}
    if database:
        query = {'database': database}

    return Response(request.route_url('login', _query=query))
