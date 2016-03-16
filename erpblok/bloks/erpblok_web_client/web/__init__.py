from anyblok.declarations import Declarations
from anyblok import reload_module_if_blok_is_reloading
from anyblok.blok import BlokManager
from erpblok.client.template import Template


@Declarations.register(Declarations.Model)
class Web:

    @classmethod
    def format_static(cls, blok, static_url):
        """ Replace the attribute #BLOK by the real name of the blok """
        if static_url.startswith('#BLOK'):
            return '/' + blok + static_url[5:]
        else:
            return static_url

    @classmethod
    def get_static(cls, static_type):
        """ return the list of all static file path

        :param static_type: entry in the blok
        :rtype: list of the path
        """
        res = []
        Blok = cls.registry.System.Blok
        for blok in Blok.list_by_state('installed'):
            b = BlokManager.get(blok)
            if hasattr(b, static_type):
                for static_url in getattr(b, static_type):
                    res.append(cls.format_static(blok, static_url))

        return res

    @classmethod
    def get_css(cls):
        """ Return the css paths """
        return cls.get_static('global_css') + cls.get_static('client_css')

    @classmethod
    def get_js(cls):
        """ return the js paths """
        return cls.get_static('global_js') + cls.get_static('client_js')

    @classmethod
    def get_js_babel(cls):
        """ return the babel paths """
        return (cls.get_static('global_js_babel') +
                cls.get_static('client_js_babel'))

    @classmethod
    def get_templates(cls):
        """ Return the list of the web client template to load """
        from os.path import join
        tmpl = Template(forclient=True)
        Blok = cls.registry.System.Blok
        for blok in Blok.list_by_state('installed'):
            b = BlokManager.get(blok)
            if hasattr(b, 'client_templates'):
                bpath = BlokManager.getPath(blok)
                for template in b.client_templates:
                    with open(join(bpath, template), 'r') as fp:
                        tmpl.load_file(fp)

        tmpl.compile()
        return tmpl.get_all_template()

from . import space  # noqa
reload_module_if_blok_is_reloading(space)
from . import login  # noqa
reload_module_if_blok_is_reloading(login)
from . import user  # noqa
reload_module_if_blok_is_reloading(user)
