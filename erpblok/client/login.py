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
    title = ArgsParseManager.get('app_name', 'ERPBlok')
    return {
        'title': title,
        'databases': list_databases(),
        'database': database,
    }


@Declarations.Pyramid.add_view('login-logo')
def get_login_logo(request):
    url_login_logo = ArgsParseManager.get('url_login_logo')
    if url_login_logo:
        return HTTPFound(location=url_login_logo)

    return HTTPFound(location="/static/login-logo.png")


@Declarations.Pyramid.add_view('login-connect')
def post_login_connect(request, database=None, login=None, password=None):
    registry = RegistryManager.get(database)
    authentificated = registry.Web.Login.check_authentification(
        login, password)
    if authentificated:
        login_user(request, database, login, password)
        return Response(request.route_url('web-client'))
    else:
        return HTTPUnauthorized()


@Declarations.Pyramid.add_view('login-disconnect')
def post_login_disconnect(request, database=None, login=None, password=None):
    logout(request)
    database = request.session.get('database')
    query = {}
    if database:
        query = {'database': database}

    return Response(request.route_url('login', _query=query))
