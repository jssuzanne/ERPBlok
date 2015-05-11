from anyblok.blok import Blok


class ERPBlokDemo(Blok):
    """ Demo blok for ERPBlok """
    version = '0.0.1'

    required = [
        'anyblok-io-xml',
        'erpblok-core',
    ]

    def install(self):
        """ Initialize database with the blok information """
        self.import_cfg_file('xml', 'Model.Access.User', 'user.xml')

    def update(self, latest_version):
        """ Update the database """
        if latest_version is None:
            self.install()

    @classmethod
    def reload_declaration_module(cls, reload):
        pass
