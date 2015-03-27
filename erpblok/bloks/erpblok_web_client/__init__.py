from anyblok.blok import Blok


class ERPBlokWebClient(Blok):
    version = '0.0.1'
    autoinstall = True

    required = [
        'anyblok-core',
        'anyblok-io',
        'pyramid',
    ]

    css = [
        '/static/materialize-src/css/materialize.css',
        '/static/erpblok.css',
        '#BLOK/static/breadcrumb.css',
    ]

    js = [
        '/static/jquery-2.1.3.min.js',
        '/static/materialize-src/js/bin/materialize.min.js',
        '/static/client.js',
        '#BLOK/static/erpblok.js',
        '#BLOK/static/rpc.js',
        '#BLOK/static/hashtag-manager.js',
        '#BLOK/static/menu.js',
        '#BLOK/static/breadcrumb.js',
        '#BLOK/static/action.js',
        '#BLOK/static/dialog.js',
        '#BLOK/static/view.js',
        '#BLOK/static/view_list.js',
        '#BLOK/static/view_form.js',
        #'#BLOK/static/notification/notification.js',
    ]

    def install_access_groups(self):
        Group = self.registry.Access.Group
        return Group.insert(name='administration', label='Administration')

    def install_admin_user(self, group):
        login = self.registry.Web.Login.insert(login='admin', password='admin')
        user = self.registry.Access.User.insert(last_name='Administrator',
                                                login=login)
        user.groups.append(group)
        self.registry.IO.Mapping.set('main_admin_user', user)

    def install_user_menu(self):
        UserMenu = self.registry.UI.UserMenu
        UserMenu.insert(function='do_about',
                        icon='mdi-social-public',
                        label='About')
        UserMenu.insert(function='do_logout',
                        order=1000,
                        label='Log out')

    def install_quick_menu(self):
        QuickMenu = self.registry.UI.QuickMenu
        QuickMenu.insert(function='do_something',
                         icon='mdi-communication-email',
                         title='Quick 1')
        QuickMenu.insert(action=2,
                         icon='mdi-notification-mms',
                         title='Quick 2')
        QuickMenu.insert(menu=3,
                         icon='mdi-social-cake',
                         title='Quick 3')
        QuickMenu.insert(function='do_something',
                         icon='mdi-social-person',
                         title='Quick 4')

    def install_menus(self):
        Menu = self.registry.UI.Menu
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
        group = self.install_access_groups()
        self.install_admin_user(group)
        self.install_user_menu()
        self.install_menus()
        self.install_quick_menu()

    def update(self, latest_version):
        if latest_version is None:
            self.install()

    @classmethod
    def import_declaration_module(cls):
        from . import web  # noqa
        from . import access  # noqa
        from . import ui  # noqa
        from . import controllers  # noqa

    @classmethod
    def reload_declaration_module(cls, reload):
        from . import web
        reload(web)
        from . import access
        reload(access)
        from . import ui
        reload(ui)
        from . import controllers
        reload(controllers)
