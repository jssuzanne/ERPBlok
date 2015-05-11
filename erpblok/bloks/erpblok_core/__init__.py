from anyblok.blok import Blok


class ERPBlokCore(Blok):
    """ Base Blok for ERPBlok """
    version = '0.0.1'
    autoinstall = True

    required = [
        'erpblok-web-client',
        'anyblok-io-xml',
    ]

    def update(self, latest_version):
        super(ERPBlokCore, self).update(latest_version)
        self.import_cfg_file('xml', 'Model.Access.Group', 'groups.xml')
        self.import_cfg_file('xml', 'Model.Access.User', 'user.xml')
        self.import_cfg_file('xml', 'Model.UI.UserMenu', 'user_menu.xml')
        self.import_cfg_file('xml', 'Model.UI.Action', 'action_access.xml')
        self.import_cfg_file('xml', 'Model.UI.Action',
                             'action_configuration.xml')
        self.import_cfg_file('xml', 'Model.UI.Menu', 'menu.xml')
