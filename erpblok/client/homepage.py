from anyblok import Declarations
from pyramid.httpexceptions import HTTPFound
from .common import list_databases
from anyblok._argsparse import ArgsParseManager


Declarations.Pyramid.add_route('homepage', '/')


@Declarations.Pyramid.add_view('homepage')
def get_homepage(request):
    """ Redirect the homepage to the good page """
    databases = list_databases()
    session = request.session
    connection_state = session.get('state', 'disconnected')
    connection_database = session.get('database')
    config_database = ArgsParseManager.get('db_name')

    if connection_database and connection_state == 'connected':
        # redirect => client
        url = request.route_url('web-client')
    elif databases:
        if connection_database and connection_database in databases:
            # redirect to login with database selection
            url = request.route_url(
                'login', _query={'database': connection_database})
        elif config_database and config_database in databases:
            # redirect to login with database selection
            url = request.route_url(
                'login', _query={'database': config_database})
        elif len(databases) == 1:
            # redirect to login with database selection
            url = request.route_url(
                'login', _query={'database': databases[0]})
        else:
            # redirect to login without database selection
            url = request.route_url('login')
    else:
        # redirect to database manager
        url = request.route_url('database')

    return HTTPFound(location=url)
