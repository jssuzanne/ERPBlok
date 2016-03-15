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

    def update(self, latest_version):
        """ Update the database """
        self.import_file('xml', 'Model.Web.User', 'user.xml')
