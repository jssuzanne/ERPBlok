from anyblok import Declarations


register = Declarations.register
Web = Declarations.Model.Web
Integer = Declarations.Column.Integer
String = Declarations.Column.String
Many2One = Declarations.RelationShip.Many2One


@register(Web)
class Menu:

    id = Integer(primary_key=True)
    order = Integer(nullable=False, default=10)
    function = String()
    action = Integer()
    parent = Many2One(model='Model.Web.Menu', one2many='children')
    label = String(nullable=False)

    @Declarations.hybrid_method()
    def with_login(self, login):
        # TODO, add filter by login
        return True


@register(Web)
class UserMenu:

    id = Integer(primary_key=True)
    order = Integer(nullable=False, default=10)
    function = String(nullable=False)
    icon = String()
    label = String(nullable=False)

    @Declarations.hybrid_method()
    def with_login(self, login):
        # TODO, add filter by login
        return True


@register(Web)
class QuickMenu:

    id = Integer(primary_key=True)
    order = Integer(nullable=False, default=10)
    function = String()
    action = Integer()
    menu = Integer(foreign_key=(Web.Menu, 'id'))
    icon = String(nullable=False)
    title = String()

    @Declarations.hybrid_method()
    def with_login(self, login):
        # TODO, add filter by login
        return True
