import os


def add_mako_and_static(config):
    config.include('pyramid_mako')
    here = os.path.dirname(__file__)
    config.add_static_view('static', os.path.join(here, 'static'))
