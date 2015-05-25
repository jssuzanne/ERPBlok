from anyblok_pyramid.scripts import anyblok_wsgi
from anyblok_pyramid.config import make_config as ap_make_config
from . import _argsparse  # noqa
import os


def make_config():
    """ Add includem for mako and global static route """
    config = ap_make_config()
    config.include('pyramid_mako')
    here = os.path.dirname(__file__)
    config.add_static_view('static', os.path.join(here, 'static'))
    return config


def wsgi():
    """ wsgi console script """
    from . import client  # noqa
    anyblok_wsgi('Web server for AnyBlok', '0.0.1',
                 ['config', 'database', 'logging', 'database-manager'],
                 Configurator=make_config)
