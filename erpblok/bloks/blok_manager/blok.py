from anyblok import Declarations
from anyblok.field import Function
from anyblok.blok import BlokManager
from anyblok.registry import RegistryManager
from docutils.core import publish_programmatically
from docutils import io
from rst2html5 import HTML5Writer
from os.path import join, isfile
from lxml import html


register = Declarations.register
System = Declarations.Model.System


@Declarations.register(Declarations.Model.System)
class Blok:

    logo = Function(fget='get_logo')

    def get_logo(self):
        blok = BlokManager.get(self.name)

        def _get_logo(blok_name, logo_path):
            path = BlokManager.getPath(blok_name)
            file_path = join(path, logo_path)
            if isfile(file_path):
                return self.registry.UI.Image.filepath2html(file_path)
            else:
                return None

        if hasattr(blok, 'logo'):
            return _get_logo(self.name, blok.logo)
        else:
            return _get_logo('erpblok-blok-manager', 'static/image/none.png')

    def convert_rst2html(self, rst):
        output, _ = publish_programmatically(
            source_class=io.StringInput, source=rst, source_path=None,
            destination_class=io.StringOutput, destination=None,
            destination_path=None, reader=None, reader_name='standalone',
            parser=None, parser_name='restructuredtext',
            writer=HTML5Writer(), writer_name='null',
            settings=None, settings_spec=None, settings_overrides={},
            config_section=None, enable_exit_status=None)
        return html.tostring(html.fromstring(output).find('body'))

    def get_short_description(self):
        res = super(Blok, self).get_short_description()
        return self.convert_rst2html(res)

    def get_long_description(self):
        res = super(Blok, self).get_long_description()
        return self.convert_rst2html(res)

    # FIXME install, upgrade and uninstall must relod if they are view
    def install_blok(self):
        self.registry.upgrade(install=[self.name])
        return {'action': 'refresh', 'primary_keys': self.to_primary_keys()}

    def upgrade_blok(self):
        self.registry.upgrade(update=[self.name])
        return {'action': 'refresh', 'primary_keys': self.to_primary_keys()}

    def uninstall_blok(self):
        self.registry.upgrade(uninstall=[self.name])
        if self.name == 'erpblok-blok-manager':
            return {'action': 'reload', 'keephash': False}

        return {'action': 'refresh', 'primary_keys': self.to_primary_keys()}

    @classmethod
    def reload_blokmanager(cls, *args, **kwargs):
        RegistryManager.clear()  # close all the registry
        BlokManager.reload()  # reload all the blok code
        # FIXME BlokManager.reload should close all the registry and
        # forbidden load registry during the reload
        return {'action': 'reload'}
