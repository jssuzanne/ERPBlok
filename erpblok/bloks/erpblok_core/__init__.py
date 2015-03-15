from anyblok.blok import Blok


class ERPBlokCore(Blok):
    version = '0.0.1'
    autoinstall = True

    required = [
        'erpblok-web-client',
    ]

    @classmethod
    def import_declaration_module(cls):
        pass

    @classmethod
    def reload_declaration_module(cls, reload):
        pass
