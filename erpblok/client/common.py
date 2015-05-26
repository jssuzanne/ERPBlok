import anyblok
from anyblok.config import Configuration
from anyblok.registry import RegistryManager
from anyblok.environment import EnvironmentManager


def list_databases():
    """ return the name of the databases """
    drivername = Configuration.get('db_driver_name')
    bdd = anyblok.BDD[drivername]
    return bdd.listdb()


def create_database(database):
    """ Create a new database, initialize it and return an AnyBlok registry

    rtype: AnyBlok registry instance
    """
    drivername = Configuration.get('db_driver_name')
    bdd = anyblok.BDD[drivername]
    bdd.createdb(database)
    registry = RegistryManager.get(database)
    return registry


def drop_database(database):
    """ Close the registry instance of the database and drop the database"""
    registry = RegistryManager.get(database)
    registry.close()
    drivername = Configuration.get('db_driver_name')
    bdd = anyblok.BDD[drivername]
    bdd.dropdb(database)


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
