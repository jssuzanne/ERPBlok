from anyblok import Declarations
from anyblok._argsparse import ArgsParseManager
from anyblok.registry import RegistryManager
from .common import list_databases, login_user, logout
from pyramid.httpexceptions import HTTPUnauthorized, HTTPFound
from pyramid.response import Response


Declarations.Pyramid.add_route('login', '/login')
Declarations.Pyramid.add_route('login-logo', '/login/logo')
Declarations.Pyramid.add_route('login-connect', '/login/connect',
                               request_method='POST')
Declarations.Pyramid.add_route('login-disconnect', '/login/disconnect',
                               request_method='POST')


@Declarations.Pyramid.add_view('login',
                               renderer='erpblok:templates/login.mak')
def get_login(request, database=None):
    """ Display the login page

    :param database: default database filled by the url
    """
    title = ArgsParseManager.get('app_name', 'ERPBlok')
    allow_database_manager = ArgsParseManager.get('allow_database_manager',
                                                  True)
    return {
        'title': title,
        'databases': list_databases(),
        'database': database,
        'allow_database_manager': allow_database_manager,
    }


@Declarations.Pyramid.add_view('login-logo')
def get_login_logo(request):
    """ Return the logo for thelogin page """
    url_login_logo = ArgsParseManager.get('url_login_logo')
    if url_login_logo:
        return HTTPFound(location=url_login_logo)

    return HTTPFound(location="/static/login-logo.png")


@Declarations.Pyramid.add_view('login-connect')
def post_login_connect(request, database=None, login=None, password=None):
    """ Log the user, if the login and password are right

    :param database: the target database
    :param login: the login to verify
    :param password: the password to verify
    :rtype: redirection if login/password is right else HTTPUnauthorized
    """
    registry = RegistryManager.get(database)
    authentificated = registry.Web.Login.check_authentification(
        login, password)
    if authentificated:
        if login_user(request, database, login, password):
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
