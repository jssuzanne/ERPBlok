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
    def get_user_menu(cls, login):
        UserMenu = cls.registry.Web.UserMenu
        query = UserMenu.query('function', 'icon', 'label')
        query = query.filter(UserMenu.with_login(login))
        query = query.order_by(UserMenu.order)
        return query.all()

    @classmethod
    def get_quick_menu(cls, login):
        QuickMenu = cls.registry.Web.QuickMenu
        query = QuickMenu.query('function', 'action', 'menu', 'icon', 'title')
        query = query.filter(QuickMenu.with_login(login))
        query = query.order_by(QuickMenu.order)
        return query.all()

    @classmethod
    def get_app_menu(cls, login):
        res = []
        Menu = cls.registry.Web.Menu
        query = Menu.query()
        query = query.filter(Menu.web_menu_id.is_(None))
        query = query.filter(Menu.with_login(login))
        query = query.order_by(Menu.order)
        for m in query.all():
            res.append((m.function, m.action, m.id, m.label,
                        cls.get_recurse_app_menu(m)))

        return res

    @classmethod
    def get_recurse_app_menu(cls, node):
        res = []
        for m in node.children:
            res.append((m.function, m.action, m.id, m.label,
                        cls.get_recurse_app_menu(m)))

        return res

from . import login  # noqa
from . import menu  # noqa
