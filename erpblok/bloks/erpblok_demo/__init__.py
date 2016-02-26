from anyblok.blok import Blok
from anyblok.config import Configuration


class ERPBlokDemo(Blok):
    """ Demo blok for ERPBlok """
    version = '0.0.1'

    required = [
        'anyblok-io-xml',
        'erpblok-core',
    ]

    setting_blok_description = {
        'label': 'Demo datas',
        'description': 'Install the demo datas to start with some data in the '
                       'goal to test ERPBlok',
        'value': Configuration.get('db_manager_demo'),
    }

    def install(self):
        """ Initialize database with the blok information """
        self.import_file('xml', 'Model.Access.User', 'user.xml')

    def update(self, latest_version):
        """ Update the database """
        if latest_version is None:
            self.install()

    @classmethod
    def reload_declaration_module(cls, reload):
        pass
