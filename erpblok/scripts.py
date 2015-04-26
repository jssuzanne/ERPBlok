from anyblok_pyramid.scripts import anyblok_wsgi
from anyblok.scripts import (interpreter as anyblok_interpreter,
                             createdb, run_exit)
from anyblok_pyramid.config import make_config as ap_make_config
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
                 ['config', 'database', 'logging'],
                 ['AnyBlok', 'ERPBlok'],
                 Configurator=make_config)


def interpreter():
    anyblok_interpreter(
        'Interpreter', '1.0',
        argsparse_groups=['config', 'database', 'interpreter', 'logging'],
        parts_to_load=['AnyBlok', 'ERPBlok'])


def anyblok_createdb():
    from anyblok_pyramid.release import version
    description = "ERPBlok - %s create db" % version
    createdb(description, ['config', 'database', 'unittest'],
             ['AnyBlok', 'ERPBlok'])


def anyblok_nose():
    from anyblok_pyramid.release import version
    run_exit("Nose test for ERPBlok", version, ['config', 'database'],
             ['AnyBlok', 'ERPBlok'])
