import os
from pyramid.renderers import JSON
from sqlalchemy_utils.types.password import Password
from pyramid_rpc.jsonrpc import DEFAULT_RENDERER


def add_mako_and_static(config):
    config.include('pyramid_mako')
    here = os.path.dirname(__file__)
    config.add_static_view('static', os.path.join(here, 'static'))


def password_adapter(obj, request):
    if obj.hash:
        return 'SECRET PASSWORD'

    return ''


def bytes_adapter(obj, request):
    if obj:
        return obj.decode('utf8')

    return ''


def declare_json_data_adapter(config):
    json_renderer = JSON()
    json_renderer.add_adapter(Password, password_adapter)
    json_renderer.add_adapter(bytes, bytes_adapter)
    config.add_renderer('json', json_renderer)
    config.add_renderer(DEFAULT_RENDERER, json_renderer)


def pyramid_rpc(config):
    config.include('pyramid_rpc.jsonrpc')
