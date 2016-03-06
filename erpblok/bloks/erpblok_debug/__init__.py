from anyblok.blok import Blok


class ERPBlokDebug(Blok):
    """ Demo blok for ERPBlok """
    version = '0.0.1'

    required = [
        'anyblok-io-xml',
        'erpblok-core',
    ]

    def install(self):
        """ Initialize database with the blok information """
        self.import_file('xml', 'Model.UI.Action', 'action.xml')
        self.import_file('xml', 'Model.Web.Space', 'space.xml')

    def update(self, latest_version):
        """ Update the database """
        if latest_version is None:
            self.install()

    @classmethod
    def reload_declaration_module(cls, reload):
        pass
