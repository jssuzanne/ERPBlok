from anyblok.blok import Blok
from anyblok.config import Configuration


class ERPBlokBlokManager(Blok):
    """ Blok manager for ERPBlok """
    version = '0.0.1'

    required = [
        'anyblok-core',
        'anyblok-io-xml',
    ]

    setting_blok_description = {
        'label': 'Blok Manager',
        'description': 'Allow to install, update or unstall bloks from the '
                       'application',
        'value': Configuration.get('db_manager_blok_manager'),
    }

    views = [
        'blok.tmpl',
    ]

    def install(self):
        """ Initialize database with the blok information """
        self.import_file('xml', 'Model.Web.Space', 'space.xml')

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
