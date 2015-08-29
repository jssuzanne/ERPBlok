from anyblok_pyramid.scripts import anyblok_wsgi
from . import config as localconfig  # noqa


def wsgi():
    """ wsgi console script """
    from . import client  # noqa
    anyblok_wsgi('Web server for AnyBlok', '0.0.1',
                 ['config', 'database', 'logging', 'database-manager'])
