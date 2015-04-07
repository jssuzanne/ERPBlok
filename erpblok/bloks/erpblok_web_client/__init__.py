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
        '/static/foundation-5/css/foundation.min.css',
        '/static/erpblok.css',
        '#BLOK/static/view.css',
        '#BLOK/static/view_list.css',
    ]

    js = [
        '/static/jquery-2.1.3.min.js',
        '/static/foundation-5/js/foundation.min.js',
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
        '#BLOK/static/template.js',
        '#BLOK/static/notification/notification.js',
    ]

    template = [
        'templates.tmpl',
    ]

    def install_admin_user(self):
        Group = self.registry.Access.Group
        group = Group.insert(name='administration', label='Administration')
        login = self.registry.Web.Login.insert(login='admin', password='admin')
        user = self.registry.Access.User.insert(last_name='Administrator',
                                                login=login)
        user.groups.append(group)
        self.registry.IO.Mapping.set('main_admin_user', user)

    def install_user_menu(self):
        UserMenu = self.registry.UI.UserMenu
        UserMenu.insert(function='do_about',
                        icon='/erpblok_web_client/static/img/about.png',
                        label='About')
        UserMenu.insert(function='do_logout',
                        order=1000,
                        label='Log out')

    def install_menus(self):
        Menu = self.registry.UI.Menu
        Action = self.registry.UI.Action
        settings = Menu.insert(label='Settings')
        access = Menu.insert(label="Access", parent=settings)
        group = Action.insert(label="Access groups", model='Model.Access.Group')
        Menu.insert(label='Groups', parent=access, action=group)
        login = Action.insert(label="Access logins", model='Model.Web.Login')
        Menu.insert(label='Logins', parent=access, action=login)
        user = Action.insert(label="Access users", model='Model.Access.User')
        Menu.insert(label='Userss', parent=access, action=user)
        interface = Menu.insert(label="Interfaces", parent=settings)
        umenus = Action.insert(label='User menus', model='Model.UI.UserMenu')
        Menu.insert(label='User menus', parent=interface, action=umenus)
        qmenus = Action.insert(label='Quick menus', model='Model.UI.QuickMenu')
        Menu.insert(label='Quick menus', parent=interface, action=qmenus)
        menus = Action.insert(label='Menus', model='Model.UI.Menu')
        Menu.insert(label='Menus', parent=interface, action=menus)

    def install(self):
        self.install_admin_user()
        self.install_user_menu()
        self.install_menus()

    def update(self, latest_version):
        if latest_version is None:
            self.install()

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
