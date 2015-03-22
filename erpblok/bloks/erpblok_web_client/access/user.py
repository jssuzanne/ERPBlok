from anyblok import Declarations


register = Declarations.register
Access = Declarations.Model.Access
Login = Declarations.Model.Web.Login
Integer = Declarations.Column.Integer
String = Declarations.Column.String
Many2One = Declarations.RelationShip.Many2One
Many2Many = Declarations.RelationShip.Many2Many


@register(Access)
class User:

    id = Integer(primary_key=True)
    first_name = String()
    last_name = String(nullable=False)
    # FIXME Update AnyBlok to next version 0.2.4 Issue #2
    login = Many2One(model=Login, nullable=False)
    groups = Many2Many(model=Access.Group)
