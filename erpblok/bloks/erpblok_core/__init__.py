from anyblok.blok import Blok, BlokManager
from os.path import join


class ERPBlokCore(Blok):
    """ Base Blok for ERPBlok """
    version = '0.0.1'
    autoinstall = True

    required = [
        'erpblok-web-client',
        'anyblok-io-xml',
    ]

    views = [
        'system/blok.tmpl',
    ]

    @classmethod
    def import_declaration_module(cls):
        from . import system  # noqa

    @classmethod
    def reload_declaration_module(cls, reload):
        from . import system
        reload(system)

    def update(self, latest_version):
        blok_path = BlokManager.getPath('erpblok-core')
        with open(join(blok_path, 'menu.xml'), 'r') as fp:
            importer = self.registry.IO.Importer.XML.insert(
                model='Model.UI.Menu', file_to_import=fp.read().encode('utf-8'))
            importer.run()
