from anyblok.config import Configuration
from anyblok.blok import BlokManager
from pyramid.view import view_config
from pyramid.httpexceptions import (HTTPForbidden,
                                    HTTPFound,
                                    HTTPNotFound,
                                    HTTPUnauthorized)
from pyramid.response import Response
from .common import (list_databases, create_database, drop_database,
                     login_user, get_templates_from, get_static)


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


@view_config(route_name='database', renderer='erpblok:client.mak')
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


@view_config(route_name='database-menus', request_method="GET", renderer="json")
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


@view_config(route_name='database-addons', request_method="GET", renderer="json")
def get_addons(request):
    res = []
    for blok_name in BlokManager.ordered_bloks:
        blok = BlokManager.get(blok_name)
        if hasattr(blok, 'setting_blok_description'):
            addons = blok.setting_blok_description
            addons['id'] = blok_name
            res.append(addons)

    return res


@view_config(route_name='database-selection', request_method="GET", renderer="json")
def get_databases(request):
    return {
        'id': 'database',
        'type': 'Selection',
        'nullable': False,
        'selections': [(x, x) for x in [''] + list_databases()],
    }


@view_config(route_name='database-createdb')
def post_create_database(request):
    """ Create a new database, and initialize it

    :rtype: Redirection to the client
    """
    params = dict(request.params)
    database = params.get('database')
    login = params.get('login')
    password = params.get('password')
    db_manager_password = params.get('db_manager_password')
    install_bloks = params.get('install_bloks')
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


@view_config(route_name='database-dropdb')
def post_drop_database(request):
    """ Drop the database

    """
    params = dict(request.params)
    database = params.get('database')
    db_manager_password = params.get('db_manager_password')
    check_allow_database_manager()
    check_db_manager_password(db_manager_password)
    drop_database(database)
    return HTTPFound(location=request.route_url('database'))


@view_config(route_name='database-listdb', renderer="erpblok:templates/database-list.mak")
def post_list_database(request):
    """ Return the html of the select node with the list of the database """
    return {'databases': list_databases()}
