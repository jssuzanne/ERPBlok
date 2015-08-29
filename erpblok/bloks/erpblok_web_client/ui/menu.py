from anyblok.declarations import Declarations, hybrid_method
from anyblok.column import Integer, String
from anyblok.relationship import Many2Many, Many2One

register = Declarations.register
UI = Declarations.Model.UI
Group = Declarations.Model.Access.Group
Mixin = Declarations.Mixin


@register(Mixin)
class MixinMenu:
    id = Integer(primary_key=True)
    order = Integer(nullable=False, default=10)
    function = String()
    groups = Many2Many(model=Group)


@register(UI)
class Menu(Mixin.MixinMenu):

    action = Many2One(model=UI.Action, one2many="menus")
    parent = Many2One(model='Model.UI.Menu', one2many='children')
    label = String(nullable=False)

    @hybrid_method()
    def with_user(self):
        # TODO, add filter by login
        return True

    @hybrid_method()
    def without_group(self):
        # TODO, add filter by login
        return True


@register(UI)
class UserMenu(Mixin.MixinMenu):

    icon = String()
    label = String(nullable=False)
    action = Many2One(model=UI.Action, one2many="user_menus")

    @hybrid_method()
    def with_user(self):
        # TODO, add filter by login
        return True

    @hybrid_method()
    def without_group(self):
        # TODO, add filter by login
        return True


@register(UI)
class QuickMenu(Mixin.MixinMenu):

    action = Many2One(model=UI.Action, one2many="quick_menus")
    menu = Integer(foreign_key=UI.Menu.use('id'))
    icon = String(nullable=False)
    title = String()

    @hybrid_method()
    def with_user(self):
        # TODO, add filter by login
        return True

    @hybrid_method()
    def without_group(self):
        # TODO, add filter by login
        return True
