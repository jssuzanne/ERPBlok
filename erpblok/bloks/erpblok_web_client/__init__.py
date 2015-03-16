from anyblok.blok import Blok


class ERPBlokWebClient(Blok):
    version = '0.0.1'
    autoinstall = True

    required = [
        'anyblok-core',
        'pyramid',
    ]

    css = [
        '#BLOK/static/jquery-ui-1.11.4.custom/jquery-ui.min.css',
        '#BLOK/static/jquery-ui-1.11.4.custom/jquery-ui.structure.min.css',
        '/static/client.css',
    ]

    js = [
        '/static/jquery-2.1.3.min.js',
        '/static/client.js',
        '#BLOK/static/jquery-ui-1.11.4.custom/jquery-ui.min.js',
        '#BLOK/static/erpblok.js',
        '#BLOK/static/rpc.js',
        '#BLOK/static/notification/notification.js',
        '#BLOK/static/menu.js',
        '#BLOK/static/hashtag-manager.js',
        '#BLOK/static/breadcrums.js',
        '#BLOK/static/action.js',
    ]

    def install_user_menu(self):
        UserMenu = self.registry.Web.UserMenu
        UserMenu.insert(function='do_about',
                        icon='/static/login-logo.png',
                        label='About')
        UserMenu.insert(function='do_logout',
                        order=1000,
                        label='Log out')

    def install_quick_menu(self):
        QuickMenu = self.registry.Web.QuickMenu
        QuickMenu.insert(function='do_something',
                         icon='/static/login-logo.png',
                         title='Quick 1')
        QuickMenu.insert(action=1,
                         icon='/static/login-logo.png',
                         title='Quick 2')
        QuickMenu.insert(menu=3,
                         icon='/static/login-logo.png',
                         title='Quick 3')
        QuickMenu.insert(function='do_something',
                         icon='/static/login-logo.png',
                         title='Quick 4')

    def install_menus(self):
        Menu = self.registry.Web.Menu
        for x in range(5):
            menux = Menu.insert(label="Menu %d" % x)
            for y in range(5):
                menuy = Menu.insert(label="Menu %d SubMenu %d" % (x, y),
                                    parent=menux)
                for z in range(5):
                    menuz = Menu.insert(
                        label="Menu %d SubMenu %d SubSubMenu %d" % (x, y, z),
                        parent=menuy)
                    for t in range(5):
                        Menu.insert(
                            label="Menu %d SubMenu %d SubSubMenu %d - %d" % (x, y, z, t),
                            action=1,
                            parent=menuz)

    def install(self):
        self.install_user_menu()
        self.install_menus()
        self.install_quick_menu()

    def update(self, latest_version):
        if latest_version is None:
            self.install()

    @classmethod
    def import_declaration_module(cls):
        from . import web  # noqa
        from . import controllers  # noqa

    @classmethod
    def reload_declaration_module(cls, reload):
        from . import web
        reload(web)
        from . import controllers
        reload(controllers)
