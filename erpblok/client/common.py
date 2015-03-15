import anyblok
from anyblok._argsparse import ArgsParseManager
from anyblok.registry import RegistryManager


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
    request.session.save()


def logout(request):
    request.session['password'] = ""
    request.session['state'] = "disconnected"
    request.session.save()
