from anyblok.config import Configuration
from anyblok.registry import RegistryManager
from anyblok.environment import EnvironmentManager
from sqlalchemy import create_engine
from sqlalchemy_utils.functions import (
    database_exists, create_database as SU_create_database,
    drop_database as SU_drop_database)


def list_databases():
    """ return the name of the databases """
    url = Configuration.get_url()
    db_filter = Configuration.get('db_filter')
    text = None
    if url.drivername in ('postgres', 'postgresql'):
        url = Configuration.get_url(db_name='postgres')
        text = "SELECT datname FROM pg_database"

        #if db_filter:
        #    text += " where datname like '%s'" % db_filter

    if text is None:
        return []

    engine = create_engine(url)
    return [x[0] for x in engine.execute(text).fetchall()
            if x[0] not in ('template1', 'template0', 'postgres')]


def create_database(database):
    """ Create a new database, initialize it and return an AnyBlok registry

    rtype: AnyBlok registry instance
    """
    url = Configuration.get_url(db_name=database)
    if database_exists(url):
        raise Exception("Database %r already exist")

    db_template_name = Configuration.get('db_template_name', None)
    SU_create_database(url, template=db_template_name)
    registry = RegistryManager.get(database)
    return registry


def drop_database(database):
    """ Close the registry instance of the database and drop the database"""
    url = Configuration.get_url(db_name=database)
    if not database_exists(url):
        raise Exception("Database %r does not already exist")

    registry = RegistryManager.get(database)
    registry.close()
    SU_drop_database(url)


def login_user(request, database, login, password):
    """ Log the user

    The informations of the user are saved in the request if the user is found
    by is login and is password. The user founded are saved in the Environnemnt

    :param database: the database where the user want to be connected
    :param login: user login
    :param password: user password
    :type: boolean, True if the user is founed else False
    """
    request.session['database'] = database
    request.session['login'] = login
    request.session['password'] = password
    request.session['state'] = "connected"
    registry = RegistryManager.get(database)
    User = registry.Access.User
    Login = registry.Web.Login
    query = User.query().join(Login)
    query = query.filter(Login.login == login)
    if not query.count():
        return False

    EnvironmentManager.set('user', query.first())
    request.session.save()
    return True


def logout(request):
    """ Remove the user information of the login """
    request.session['password'] = ""
    request.session['state'] = "disconnected"
    request.session.save()
