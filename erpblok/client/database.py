from anyblok import Declarations
from anyblok._argsparse import ArgsParseManager
from pyramid.httpexceptions import HTTPForbidden, HTTPFound, HTTPNotFound
from pyramid.response import Response
from .common import list_databases, create_database, drop_database, login_user


Declarations.Pyramid.add_route('database', '/database/manager')
Declarations.Pyramid.add_route('database-listdb', '/database/manager/list',
                               request_method='POST')
Declarations.Pyramid.add_route('database-createdb', '/database/manager/create',
                               request_method='POST')
Declarations.Pyramid.add_route('database-dropdb', '/database/manager/drop',
                               request_method='POST')


def check_allow_database_manager():
    """ raise an execption if the database manager is unactive
    :exception: pyramid.httpexceptions.HTTPNotFound
    """
    allow_database_manager = ArgsParseManager.get('allow_database_manager',
                                                  True)
    if not allow_database_manager:
        raise HTTPNotFound()


@Declarations.Pyramid.add_view('database',
                               renderer='erpblok:templates/database.mak')
def get_database(request):
    """ Return the main page of the database manager """

    check_allow_database_manager()
    title = ArgsParseManager.get('app_name', 'ERPBlok')
    return {'title': title}


@Declarations.Pyramid.add_view('database-createdb')
def post_create_database(request, database=None, login=None, password=None):
    """ Create a new database, and initialize it

    :param database: name of the database to create
    :param login: login wanted for the aministrator
    :param password: password wanted for the administrator
    :rtype: Redirection to the client
    """
    check_allow_database_manager()
    if database in list_databases():
        return HTTPForbidden()

    registry = create_database(database)
    registry.Web.Login.update_admin(login, password)
    registry.commit()
    login_user(request, database, login, password)
    return Response(request.route_url('web-client'))


@Declarations.Pyramid.add_view('database-dropdb')
def post_drop_database(request, database):
    """ Drop the database

    :param database: database name to drop
    """
    check_allow_database_manager()
    drop_database(database)
    return HTTPFound(location=request.route_url('database'))


@Declarations.Pyramid.add_view('database-listdb',
                               renderer="erpblok:templates/database-list.mak")
def post_list_database(request):
    """ Return the html of the select node with the list of the database """
    return {'databases': list_databases()}
