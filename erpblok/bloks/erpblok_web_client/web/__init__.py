from anyblok import Declarations
from anyblok.blok import BlokManager


@Declarations.register(Declarations.Model)
class Web:

    @classmethod
    def format_static(cls, blok, static_url):
        if static_url.startswith('#BLOK'):
            return '/' + blok + static_url[5:]
        else:
            return static_url

    @classmethod
    def get_static(cls, static_type):
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
        return cls.get_static('css')

    @classmethod
    def get_js(cls):
        return cls.get_static('js')

    @Declarations.classmethod_cache()
    def get_user_menu(cls):
        UserMenu = cls.registry.UI.UserMenu
        query = query2 = UserMenu.query('function', 'action', 'icon', 'label')
        query = query.filter(UserMenu.with_user())
        query2 = query2.filter(UserMenu.without_group())
        query.union_all(query2)
        query = query.order_by(UserMenu.order)
        return query.all()

    @classmethod
    def get_quick_menu(cls):
        QuickMenu = cls.registry.UI.QuickMenu
        query = query2 = QuickMenu.query('function', 'action', 'menu', 'icon', 'title')
        query = query.filter(QuickMenu.with_user())
        query2 = query2.filter(QuickMenu.without_group())
        query.union_all(query2)
        query = query.order_by(QuickMenu.order)
        return query.all()

    @classmethod
    def get_app_menu(cls):
        res = []
        Menu = cls.registry.UI.Menu
        query = Menu.query()
        query = query2 = query.filter(Menu.ui_menu_id.is_(None))
        query = query.filter(Menu.with_user())
        query2 = query2.filter(Menu.without_group())
        query.union_all(query2)
        query = query.order_by(Menu.order)
        for m in query.all():
            res.append((m.id, m.label, cls.get_recurse_app_menu(m)))

        return res

    @classmethod
    def get_recurse_app_menu(cls, node):
        res = []
        for m in node.children:
            res.append((m.id, m.label, cls.get_recurse_app_menu(m)))

        return res

    @classmethod
    def get_templates(cls):
        from os.path import join
        tmpl = cls.registry.UI.Template(forclient=True)
        Blok = cls.registry.System.Blok
        for blok in Blok.list_by_state('installed'):
            b = BlokManager.get(blok)
            if hasattr(b, 'template'):
                bpath = BlokManager.getPath(blok)
                for template in b.template:
                    with open(join(bpath, template), 'r') as fp:
                        tmpl.load_file(fp)

        tmpl.compile()
        return tmpl.get_all_template()

from . import login  # noqa
