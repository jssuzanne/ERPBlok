from anyblok import Declarations
from anyblok.config import Configuration
from anyblok.blok import BlokManager
from pyramid.httpexceptions import (HTTPForbidden,
                                    HTTPFound,
                                    HTTPNotFound,
                                    HTTPUnauthorized)
from pyramid.response import Response
from .common import (list_databases, create_database, drop_database,
                     login_user, get_templates_from, get_static)


Declarations.Pyramid.add_route('database', '/database/manager')
Declarations.Pyramid.add_route('database-listdb', '/database/manager/list',
                               request_method='POST')
Declarations.Pyramid.add_route('database-menus', '/database/menus')
Declarations.Pyramid.add_route('database-addons', '/database/addons')
Declarations.Pyramid.add_route('database-selection', '/database/selection')
Declarations.Pyramid.add_route('database-createdb', '/database/manager/create',
                               request_method='POST')
Declarations.Pyramid.add_route('database-dropdb', '/database/manager/drop',
                               request_method='POST')


def check_allow_database_manager():
    """ raise an execption if the database manager is unactive
    :exception: pyramid.httpexceptions.HTTPNotFound
    """
    allow_database_manager = Configuration.get('allow_database_manager')
    if not allow_database_manager:
        raise HTTPNotFound()


def check_db_manager_password(password):
    db_manager_password = Configuration.get('db_manager_password')
    if password != db_manager_password:
        raise HTTPUnauthorized()


@Declarations.Pyramid.add_view('database', renderer='erpblok:client.mak')
def get_database(request):
    """ Return the main page of the database manager """

    check_allow_database_manager()
    title = Configuration.get('app_name', 'ERPBlok')
    return {
        'title': title,
        'css': get_static('global_css') + get_static('database_css'),
        'js': get_static('global_js') + get_static('database_js'),
        'js_babel': (get_static('global_js_babel') +
                     get_static('database_js_babel')),
        'templates': get_templates_from('database_templates'),
    }


@Declarations.Pyramid.add_view('database-menus', request_method="GET",
                               renderer="json")
def get_menus(request):
    res = [
        {
            'label': 'Tools',
            'icon': 'fi-wrench',
            'menus': [
                {
                    'id': 'open_create_page',
                    'icon': 'fi-plus',
                    'label': 'Create a new database',
                    'description': 'Create a new database, and start to '
                                   'configure it',
                },
                {
                    'id': 'open_drop_page',
                    'icon': 'fi-trash',
                    'label': 'Drop an existing database',
                },
            ],
        },
        {
            'label': 'Other',
            'menus': [
                {
                    'id': 'return_to_login_page',
                    'label': 'Close and return to the login page',
                },
            ],
        },
    ]
    return res


@Declarations.Pyramid.add_view('database-addons', request_method="GET",
                               renderer="json")
def get_addons(request):
    res = []
    for blok_name in BlokManager.ordered_bloks:
        blok = BlokManager.get(blok_name)
        if hasattr(blok, 'setting_blok_description'):
            addons = blok.setting_blok_description
            addons['id'] = blok_name
            res.append(addons)

    return res


@Declarations.Pyramid.add_view('database-selection', request_method="GET",
                               renderer="json")
def get_databases(request):
    return {
        'id': 'database',
        'type': 'Selection',
        'nullable': False,
        'selections': [(x, x) for x in [''] + list_databases()],
    }


@Declarations.Pyramid.add_view('database-createdb')
def post_create_database(request, database=None, login=None, password=None,
                         db_manager_password=None, install_bloks=None,
                         **kwargs):
    """ Create a new database, and initialize it

    :param database: name of the database to create
    :param login: login wanted for the aministrator
    :param password: password wanted for the administrator
    :rtype: Redirection to the client
    """
    check_allow_database_manager()
    check_db_manager_password(db_manager_password)
    if database in list_databases():
        return HTTPForbidden()

    registry = create_database(database)
    registry.Web.Login.update_admin(login, password)
    registry.commit()

    if install_bloks:
        install_bloks = install_bloks.split(',')
        registry.upgrade(install=install_bloks)
        registry.commit()

    user = registry.IO.Mapping.get('Model.Web.User', 'main_admin_user')
    login_user(request, database, login, password, user.id)
    return Response(request.route_url('web-client'))


@Declarations.Pyramid.add_view('database-dropdb')
def post_drop_database(request, database=None, db_manager_password=None):
    """ Drop the database

    :param database: database name to drop
    """
    check_allow_database_manager()
    check_db_manager_password(db_manager_password)
    drop_database(database)
    return HTTPFound(location=request.route_url('database'))


@Declarations.Pyramid.add_view('database-listdb',
                               renderer="erpblok:templates/database-list.mak")
def post_list_database(request):
    """ Return the html of the select node with the list of the database """
    return {'databases': list_databases()}
