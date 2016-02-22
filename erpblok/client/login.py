from anyblok import Declarations
from anyblok.config import Configuration
from anyblok.registry import RegistryManager
from .common import list_databases, login_user, logout
from pyramid.httpexceptions import HTTPUnauthorized, HTTPFound
from pyramid.response import Response
from anyblok.blok import BlokManager
from os.path import join
from .template import Template


Declarations.Pyramid.add_route('login', '/login')
Declarations.Pyramid.add_route('login-logo', '/login/logo')
Declarations.Pyramid.add_route('login-databases', '/login/databases')
Declarations.Pyramid.add_route('login-connect', '/login/connect',
                               request_method='POST')
Declarations.Pyramid.add_route('login-disconnect', '/login/disconnect',
                               request_method='POST')


def format_static(blok, static_url):
    """ Replace the attribute #BLOK by the real name of the blok """
    if static_url.startswith('#BLOK'):
        return '/' + blok + static_url[5:]
    else:
        return static_url


def get_static(static_type):
    res = []
    for blok_name in BlokManager.ordered_bloks:
        blok = BlokManager.get(blok_name)
        if hasattr(blok, static_type):
            for static_url in getattr(blok, static_type):
                res.append(format_static(blok_name, static_url))

    return res


def get_templates_from(attr):
    tmpl = Template(forclient=True)
    for blok_name in BlokManager.ordered_bloks:
        blok = BlokManager.get(blok_name)
        if hasattr(blok, attr):
            bpath = BlokManager.getPath(blok_name)
            for template in getattr(blok, attr):
                with open(join(bpath, template), 'r') as fp:
                    tmpl.load_file(fp)

    tmpl.compile()
    return tmpl.get_all_template()


@Declarations.Pyramid.add_view('login',
                               renderer='erpblok:templates/client2.mak')
def get_login(request, database=None):
    """ Display the login page

    """
    title = Configuration.get('app_name', 'ERPBlok')
    return {
        'title': title,
        'css': get_static('login_css'),
        'js': get_static('login_js'),
        'js_babel': get_static('login_js_babel'),
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
    return list_databases()


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
