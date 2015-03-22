import anyblok
from anyblok._argsparse import ArgsParseManager
from anyblok.registry import RegistryManager
from anyblok.environment import EnvironmentManager


def list_databases():
    drivername = ArgsParseManager.get('dbdrivername')
    bdd = anyblok.BDD[drivername]
    return bdd.listdb()


def create_database(database):
    drivername = ArgsParseManager.get('dbdrivername')
    bdd = anyblok.BDD[drivername]
    bdd.createdb(database)
    registry = RegistryManager.get(database)
    return registry


def drop_database(database):
    registry = RegistryManager.get(database)
    registry.close()
    drivername = ArgsParseManager.get('dbdrivername')
    bdd = anyblok.BDD[drivername]
    bdd.dropdb(database)


def login_user(request, database, login, password):
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
    request.session['password'] = ""
    request.session['state'] = "disconnected"
    request.session.save()
