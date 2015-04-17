from anyblok import Declarations
from docutils.core import publish_programmatically
from docutils import io
from rst2html5 import HTML5Writer


@Declarations.register(Declarations.Model.System)
class Blok:

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
