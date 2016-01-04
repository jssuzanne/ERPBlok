from anyblok.blok import Blok, BlokManager


class ERPBlokWebClient(Blok):
    """ Web Client for ERPBlok """
    version = '0.0.1'
    autoinstall = True

    required = [
        'anyblok-core',
        'anyblok-io',
        'pyramid',
    ]

    css = [
        '/static/foundation-6/css/foundation.min.css',
        '/static/foundation-icons/foundation-icons.css',
        '/static/erpblok.css',
        '#BLOK/static/view.css',
        '#BLOK/static/view_list.css',
    ]

    js = [
        '/static/jquery-2.1.3.min.js',
        '/static/foundation-6/js/foundation.min.js',
        '/static/client.js',
        '#BLOK/static/anyblok-js.js',
        '#BLOK/static/underscore-min.js',
        '#BLOK/static/erpblok.js',
        '#BLOK/static/rpc.js',
        '#BLOK/static/hashtag-manager.js',
        '#BLOK/static/menu.js',
        '#BLOK/static/breadcrumb.js',
        '#BLOK/static/action.js',
        '#BLOK/static/dialog.js',
        '#BLOK/static/view.js',
        '#BLOK/static/view_multi_entries.js',
        '#BLOK/static/field.js',
        '#BLOK/static/view_list.js',
        '#BLOK/static/view_thumbnails.js',
        '#BLOK/static/view_form.js',
        '#BLOK/static/template.js',
        '#BLOK/static/notification/notification.js',
    ]

    template = [
        'templates.tmpl',
    ]

    def load(self):
        from os.path import join
        tmpl = self.registry.UI.Template()
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
        from . import web  # noqa
        from . import access  # noqa
        from . import ui  # noqa
        from . import controllers  # noqa

    @classmethod
    def reload_declaration_module(cls, reload):
        from . import core
        reload(core)
        from . import web
        reload(web)
        from . import access
        reload(access)
        from . import ui
        reload(ui)
        from . import controllers
        reload(controllers)
