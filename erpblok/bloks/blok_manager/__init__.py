from anyblok.blok import Blok


class ERPBlokBlokManager(Blok):
    """ Blok manager for ERPBlok """
    version = '0.0.1'

    required = [
        'anyblok-core',
        'anyblok-io-xml',
    ]

    views = [
        'blok.tmpl',
    ]

    def install(self):
        """ Initialize database with the blok information """
        self.import_file('xml', 'Model.UI.Menu', 'menu.xml')

    def update(self, latest_version):
        """ Update the database """
        if latest_version is None:
            self.install()

    @classmethod
    def import_declaration_module(cls):
        from . import blok  # noqa

    @classmethod
    def reload_declaration_module(cls, reload):
        from . import blok
        reload(blok)
