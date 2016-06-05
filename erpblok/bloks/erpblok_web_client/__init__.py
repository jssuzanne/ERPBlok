from anyblok.blok import Blok, BlokManager
from erpblok.client.template import Template
from .pyramid import json_data_adapter


class ERPBlokWebClient(Blok):
    """ Web Client for ERPBlok """
    version = '0.0.1'
    autoinstall = True

    required = [
        'anyblok-core',
        'anyblok-io',
    ]

    # Define the static for all pages
    global_css = [
        '#BLOK/static/foundation-6.1.2/css/foundation.min.css',
        '#BLOK/static/foundation-icons/foundation-icons.css',
        '#BLOK/static/jquery-ui-1.11.4/jquery-ui.min.css',
        '#BLOK/static/trumbowyg-2.0.0-beta-7/ui/trumbowyg.min.css',
        '#BLOK/static/erpblok.css',
        '#BLOK/static/fields.css',
    ]
    global_js = [
        '#BLOK/static/react.min.js',
        '#BLOK/static/react-dom.min.js',
        '#BLOK/static/babel-core/5.8.34/browser.min.js',
        '#BLOK/static/jquery-2.1.3.min.js',
        '#BLOK/static/jquery-ui-1.11.4/jquery-ui.min.js',
        '#BLOK/static/foundation-6.1.2/js/foundation.min.js',
        '#BLOK/static/jsviews.min.js',
        '#BLOK/static/trumbowyg-2.0.0-beta-7/trumbowyg.min.js',
        '#BLOK/static/anyblok-js.js',
        '#BLOK/static/erpblok.js',
        '#BLOK/static/rpc.js',
    ]

    global_js_babel = [
        '#BLOK/static/template.js',
        '#BLOK/static/fields.js',
        '#BLOK/static/modals.js',
    ]

    # Define the static for the login page
    login_css = []

    login_js = []

    login_js_babel = [
        '#BLOK/static/url-search-manager.js',
        '#BLOK/static/login.js',
    ]

    login_templates = [
        'login_templates.tmpl',
    ]

    # Define the static for database page

    database_css = []
    database_js = [
        '#BLOK/static/notification/notification.js',
    ]
    database_js_babel = [
        '#BLOK/static/database.js',
    ]
    database_templates = [
        'database_templates.tmpl',
    ]

    # Define client page
    client_css = [
        '#BLOK/static/view.css',
        '#BLOK/static/view_list.css',
    ]

    client_js = [
        '#BLOK/static/underscore-min.js',
    ]

    client_js_babel = [
        '#BLOK/static/hashtag-manager.js',
        '#BLOK/static/error-manager.js',
        '#BLOK/static/menu.js',
        '#BLOK/static/breadcrumb.js',
        '#BLOK/static/action.js',
        '#BLOK/static/dialog.js',
        '#BLOK/static/view.js',
        '#BLOK/static/view_multi_entries.js',
        '#BLOK/static/view_list.js',
        '#BLOK/static/view_thumbnails.js',
        '#BLOK/static/view_form.js',
        '#BLOK/static/notification/notification.js',
        '#BLOK/static/client.js',
        '#BLOK/static/space.js',
    ]

    client_templates = [
        'templates.tmpl',
    ]

    def load(self):
        from os.path import join
        tmpl = Template()
        Blok = self.registry.System.Blok
        for blok in Blok.list_by_state('installed'):
            b = BlokManager.get(blok)
            if hasattr(b, 'views'):
                bpath = BlokManager.getPath(blok)
                for template in b.views:
                    with open(join(bpath, template), 'r') as fp:
                        tmpl.load_file(fp)

        tmpl.compile()
        self.registry.erpblok_views = tmpl
        # TODO check all view template exist
        # TODO check if view template are not wrong

    @classmethod
    def import_declaration_module(cls):
        from . import core  # noqa
        from . import access  # noqa
        from . import web  # noqa
        from . import ui  # noqa

    @classmethod
    def reload_declaration_module(cls, reload):
        from . import core
        reload(core)
        from . import access
        reload(access)
        from . import web
        reload(web)
        from . import ui
        reload(ui)

    @classmethod
    def pyramid_load_config(cls, config):
        json_data_adapter(config)
        config.add_route('client_user_description', '/client/user/description')
        config.add_route('client_user_menus', '/client/user/menus')
        config.add_route('client_space_description',
                         '/client/space/description')
        config.add_route('client_space_menus', '/client/space/menus')
        config.add_jsonrpc_endpoint('client_space_menu', '/client/space/menu')
        config.add_jsonrpc_endpoint('web_client_action', '/web/client/action')
        config.add_jsonrpc_endpoint('web_client_view', '/web/client/view')
        config.add_jsonrpc_endpoint('web_client_field', '/web/client/field')
        config.scan(cls.__module__ + '.views')
