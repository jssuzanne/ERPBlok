from anyblok_pyramid.scripts import anyblok_wsgi
from anyblok_pyramid.config import make_config as ap_make_config
import os


def make_config():
    config = ap_make_config()
    config.include('pyramid_mako')
    here = os.path.dirname(__file__)
    config.add_static_view('static', os.path.join(here, 'static'))
    return config


def wsgi():
    from . import client  # noqa
    anyblok_wsgi('Web server for AnyBlok', '0.0.1',
                 ['config', 'database', 'logging'],
                 ['AnyBlok', 'ERPBlok'],
                 Configurator=make_config)
