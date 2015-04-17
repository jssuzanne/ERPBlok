from anyblok.blok import Blok


class ERPBlokCore(Blok):
    """ Base Blok for ERPBlok """
    version = '0.0.1'
    autoinstall = True

    required = [
        'erpblok-web-client',
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
