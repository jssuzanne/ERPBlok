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
        '/static/foundation-5/css/foundation.min.css',
        '/static/foundation-icons/foundation-icons.css',
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

    def install_admin_user(self):
        """ Create an administrator client """
        # TODO replace IT by an csv import
        Group = self.registry.Access.Group
        group = Group.insert(name='administration', label='Administration')
        login = self.registry.Web.Login.insert(login='admin', password='admin')
        user = self.registry.Access.User.insert(last_name='Administrator',
                                                login=login)
        user.groups.append(group)
        self.registry.IO.Mapping.set('main_admin_user', user)

    def install_user_menu(self):
        """ Define the user menu """
        # TODO replace IT by an csv import
        UserMenu = self.registry.UI.UserMenu
        UserMenu.insert(function='do_about',
                        icon='fi-info',
                        label='About')
        UserMenu.insert(function='do_logout',
                        order=1000,
                        label='Log out')

    def install_menus(self):
        """ Define the functionnal menus """
        # TODO replace IT by an csv import
        Menu = self.registry.UI.Menu
        Action = self.registry.UI.Action
        View = self.registry.UI.View

        settings = Menu.insert(label='Settings')

        bloks = Action.insert(label='Bloks', model='Model.System.Blok',
                              add_delete=False, add_new=False, add_edit=False)
        bthumbnails = View.insert(selectable=True,
                                  mode='Model.UI.View.Thumbnails',
                                  action=bloks,
                                  template="AnyBlokSystemBlokThumbnails",
                                  add_delete=False, add_new=False,
                                  add_edit=False)
        bform = View.insert(selectable=False, mode='Model.UI.View.Form',
                            action=bloks, template="AnyBlokSystemBlokForm",
                            add_delete=False, add_new=False, add_edit=False)
        bloks.update({'selected': bthumbnails.id})
        Action.Transition.insert(action=bloks, name='selectRecord',
                                 mode='Model.UI.View.Thumbnails',
                                 code='open_view', view=bform)
        Action.Transition.insert(action=bloks, name='newRecord',
                                 mode='Model.UI.View.Thumbnails',
                                 code='open_view', view=bform)
        others = Action.ButtonGroup.insert(label='Others',
                                           code="other",
                                           on_readonly=True)
        Action.Button.insert(label='Reload all bloks', action=bloks,
                             mode='all', group=others,
                             function="rpc_call_classmethod",
                             method='reload_blokmanager')
        Menu.insert(label="Bloks", parent=settings, action=bloks)

        access = Menu.insert(label="Access", parent=settings)
        group = Action.insert(label="Access groups",
                              model='Model.Access.Group')
        Menu.insert(label='Groups', parent=access, action=group)
        login = Action.insert(label="Access logins", model='Model.Web.Login')
        Menu.insert(label='Logins', parent=access, action=login)
        user = Action.insert(label="Access users", model='Model.Access.User')
        Menu.insert(label='Users', parent=access, action=user)

        interface = Menu.insert(label="Interfaces", parent=settings)
        umenus = Action.insert(label='User menus', model='Model.UI.UserMenu')
        Menu.insert(label='User menus', parent=interface, action=umenus)
        qmenus = Action.insert(label='Quick menus', model='Model.UI.QuickMenu')
        Menu.insert(label='Quick menus', parent=interface, action=qmenus)
        menus = Action.insert(label='Menus', model='Model.UI.Menu')
        Menu.insert(label='Menus', parent=interface, action=menus)
        actions = Action.insert(label='Actions', model='Model.UI.Action')
        Menu.insert(label='Actions', parent=interface, action=actions)
        views = Action.insert(label='Views', model='Model.UI.View')
        Menu.insert(label='View', parent=interface, action=views)

        lowlevel = Menu.insert(label="Database datas", parent=settings)
        models = Action.insert(label="Models", model='Model.System.Model')
        Menu.insert(label='Model', parent=lowlevel, action=models)
        fields = Action.insert(label="Fields", model='Model.System.Field')
        Menu.insert(label='Fields', parent=lowlevel, action=fields)
        columns = Action.insert(label="Columns", model='Model.System.Column')
        Menu.insert(label='Columns', parent=lowlevel, action=columns)
        rs = Action.insert(label="Relation Ship",
                           model='Model.System.RelationShip')
        Menu.insert(label='Relation Ship', parent=lowlevel, action=rs)
        io = Action.insert(label="In / Out mapping", model='Model.IO.Mapping')
        Menu.insert(label='In / Out mapping', parent=lowlevel, action=io)

    def install(self):
        """ Initialize database with the blok information """
        self.install_admin_user()
        self.install_user_menu()
        self.install_menus()

    def update(self, latest_version):
        """ Update the database """
        if latest_version is None:
            self.install()

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
