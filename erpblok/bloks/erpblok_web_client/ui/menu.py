from anyblok import Declarations


register = Declarations.register
UI = Declarations.Model.UI
Group = Declarations.Model.Access.Group
Mixin = Declarations.Mixin
Integer = Declarations.Column.Integer
String = Declarations.Column.String
Many2One = Declarations.RelationShip.Many2One
Many2Many = Declarations.RelationShip.Many2Many


@register(Mixin)
class MixinMenu:
    id = Integer(primary_key=True)  # Must be the alone, wait anyblok-0.2.4
    order = Integer(nullable=False, default=10)
    function = String()
    groups = Many2Many(model=Group)  # FIXME Many2Many could be work in mixin


@register(UI)
class Menu(MixinMenu):

    id = Integer(primary_key=True)
    action = Integer()
    parent = Many2One(model='Model.UI.Menu', one2many='children')
    label = String(nullable=False)
    groups = Many2Many(model=Group)

    @Declarations.hybrid_method()
    def with_user(self):
        # TODO, add filter by login
        return True

    @Declarations.hybrid_method()
    def without_group(self):
        # TODO, add filter by login
        return True


@register(UI)
class UserMenu(MixinMenu):

    id = Integer(primary_key=True)
    function = String(nullable=False)
    icon = String()
    label = String(nullable=False)
    groups = Many2Many(model=Group)

    @Declarations.hybrid_method()
    def with_user(self):
        # TODO, add filter by login
        return True

    @Declarations.hybrid_method()
    def without_group(self):
        # TODO, add filter by login
        return True


@register(UI)
class QuickMenu(MixinMenu):

    id = Integer(primary_key=True)
    action = Integer()
    menu = Integer(foreign_key=(UI.Menu, 'id'))
    icon = String(nullable=False)
    title = String()
    groups = Many2Many(model=Group)

    @Declarations.hybrid_method()
    def with_user(self):
        # TODO, add filter by login
        return True

    @Declarations.hybrid_method()
    def without_group(self):
        # TODO, add filter by login
        return True
