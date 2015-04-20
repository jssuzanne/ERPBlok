from anyblok import Declarations
from anyblok.blok import BlokManager
from docutils.core import publish_programmatically
from docutils import io
from rst2html5 import HTML5Writer
from os.path import join, isfile


register = Declarations.register
System = Declarations.Model.System
Function = Declarations.Field.Function


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
            return _get_logo('erpblok-core', 'static/image/none.png')

    def convert_rst2html(self, rst):
        output, _ = publish_programmatically(
            source_class=io.StringInput, source=rst, source_path=None,
            destination_class=io.StringOutput, destination=None,
            destination_path=None, reader=None, reader_name='standalone',
            parser=None, parser_name='restructuredtext',
            writer=HTML5Writer(), writer_name='null',
            settings=None, settings_spec=None, settings_overrides={},
            config_section=None, enable_exit_status=None)
        return output.decode('utf-8')

    def get_short_description(self):
        res = super(Blok, self).get_short_description()
        return self.convert_rst2html(res)

    def get_long_description(self):
        res = super(Blok, self).get_long_description()
        return self.convert_rst2html(res)

    def install_blok(self):
        self.registry.upgrade(install=[self.name])
        return {'action': 'reload', 'keephash': True}

    def uninstall_blok(self):
        self.registry.upgrade(uninstall=[self.name])
        return {'action': 'reload', 'keephash': True}
