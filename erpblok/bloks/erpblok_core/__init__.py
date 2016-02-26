from anyblok.blok import Blok


class ERPBlokCore(Blok):
    """ Base Blok for ERPBlok """
    version = '0.0.1'
    autoinstall = True

    required = [
        'erpblok-web-client',
        'anyblok-io-xml',
    ]

    views = [
        'views/access.tmpl',
    ]

    def update(self, latest_version):
        super(ERPBlokCore, self).update(latest_version)
        self.import_file('xml', 'Model.Access.Group', 'data', 'groups.xml')
        self.import_file('xml', 'Model.Web.Space.Category', 'data', 'spaces.category.xml')
        self.import_file('xml', 'Model.Web.Space', 'data', 'spaces.xml')
        self.import_file('xml', 'Model.Web.User', 'data', 'user.xml')
        self.import_file('xml', 'Model.UI.UserMenu', 'data', 'user_menu.xml')
        self.import_file('xml', 'Model.UI.Action', 'data', 'action_access.xml')
        self.import_file('xml', 'Model.UI.Action', 'data',
                         'action_configuration.xml')
        self.import_file('xml', 'Model.UI.Menu', 'data', 'menu.xml')
