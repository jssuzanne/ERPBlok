from anyblok import Declarations
from anyblok._argsparse import ArgsParseManager
from pyramid.httpexceptions import HTTPForbidden, HTTPFound
from pyramid.response import Response
from .common import list_databases, create_database, drop_database, login_user


Declarations.Pyramid.add_route('database', '/database/manager')
Declarations.Pyramid.add_route('database-listdb', '/database/manager/list',
                               request_method='POST')
Declarations.Pyramid.add_route('database-createdb', '/database/manager/create',
                               request_method='POST')
Declarations.Pyramid.add_route('database-dropdb', '/database/manager/drop',
                               request_method='POST')


@Declarations.Pyramid.add_view('database',
                               renderer='erpblok:templates/database.mak')
def get_database(request, database=None):
    title = ArgsParseManager.get('app_name', 'ERPBlok')
    return {'title': title}


@Declarations.Pyramid.add_view('database-createdb')
def post_create_database(request, database=None, login=None, password=None):
    if database in list_databases():
        return HTTPForbidden()

    registry = create_database(database)
    registry.Web.Login.create_admin(login, password)
    registry.commit()
    login_user(request, database, login, password)
    return Response(request.route_url('web-client'))


@Declarations.Pyramid.add_view('database-dropdb')
def post_drop_database(request, database):
    drop_database(database)
    return HTTPFound(location=request.route_url('database'))


@Declarations.Pyramid.add_view('database-listdb',
                               renderer="erpblok:templates/database-list.mak")
def post_list_database(request):
    return {'databases': list_databases()}
