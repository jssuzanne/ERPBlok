from anyblok.config import Configuration
from anyblok.registry import RegistryManager
from anyblok.blok import BlokManager
from os.path import join
from .template import Template
from sqlalchemy import create_engine
from sqlalchemy_utils.functions import (
    database_exists, create_database as SU_create_database,
    drop_database as SU_drop_database)


def list_databases():
    """ return the name of the databases found in the BDD

    the result can be filtering by the Configuration entry ``db_filter``

    ..warning::

        For the moment only the ``prostgresql`` dialect is available

    :rtype: list of the database's names
    """
    url = Configuration.get('get_url')()
    db_filter = Configuration.get('db_filter')
    text = None
    if url.drivername in ('postgres', 'postgresql'):
        url = Configuration.get('get_url')(db_name='postgres')
        text = "SELECT datname FROM pg_database"

        if db_filter:
            db_filter = db_filter.replace('%', '%%')
            text += " where datname like '%s'" % db_filter

    if text is None:
        return []

    engine = create_engine(url)
    return [x[0] for x in engine.execute(text).fetchall()
            if x[0] not in ('template1', 'template0', 'postgres')]


def create_database(database):
    """ Create a new database, initialize it and return an AnyBlok registry

    :param: database's name
    :rtype: AnyBlok registry instance
    """
    url = Configuration.get('get_url')(db_name=database)
    if database_exists(url):
        raise Exception("Database %r already exist")

    db_template_name = Configuration.get('db_template_name', None)
    SU_create_database(url, template=db_template_name)
    registry = RegistryManager.get(database)
    return registry


def drop_database(database):
    """ Close the registry instance of the database and drop the database

    :param: database's name
    """
    url = Configuration.get('get_url')(db_name=database)
    if not database_exists(url):
        raise Exception("Database %r does not already exist")

    registry = RegistryManager.get(database)
    registry.close()
    SU_drop_database(url)


def login_user(request, database, login, password, user_id):
    """ Log the user

    The informations of the user are saved in the request if the user is found
    by is login and is password.

    :param database: the database where the user want to be connected
    :param login: user login
    :param password: user password
    :type: boolean, True if the user is founed else False
    """
    # SqlAlchemy-Utils give a Password object,
    request.session['database'] = database
    request.session['login'] = login
    request.session['password'] = password
    request.session['user_id'] = user_id
    request.session['state'] = "connected"
    request.session.save()
    return True


def logout(request):
    """ Remove the user information of the login """
    request.session['password'] = ""
    request.session['login'] = ""
    request.session['user_id'] = ""
    request.session['state'] = "disconnected"
    request.session.save()
    return True


def format_static(blok, static_url):
    """ Replace the attribute #BLOK by the real name of the blok

    :param blok: the blok's name
    :param static_url: the url to format
    :rtype: str, formated url
    """
    if static_url.startswith('#BLOK'):
        return '/' + blok + static_url[5:]
    else:
        return static_url


def get_static(static_type):
    """ Get in the Blok definition the static data from the client

    :param static: entry to read: css, js, ...
    :rtype: list of str
    """
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
