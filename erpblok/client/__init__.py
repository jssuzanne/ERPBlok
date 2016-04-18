# flake8:noqa

def load_client(config):
    config.add_route('homepage', '/')
    config.add_route('web-client', '/web/client')
    config.add_route('login', '/login')
    config.add_route('login-logo', '/login/logo')
    config.add_route('login-databases', '/login/databases',
                     request_method='GET')
    config.add_route('login-connect', '/login/connect', request_method='POST')
    config.add_route('login-disconnect', '/login/disconnect',
                     request_method='POST')
    config.add_route('database', '/database/manager')
    config.add_route('database-listdb', '/database/manager/list',
                     request_method='POST')
    config.add_route('database-menus', '/database/menus')
    config.add_route('database-addons', '/database/addons')
    config.add_route('database-selection', '/database/selection')
    config.add_route('database-createdb', '/database/manager/create',
                     request_method='POST')
    config.add_route('database-dropdb', '/database/manager/drop',
                     request_method='POST')
    config.scan('erpblok.client')
