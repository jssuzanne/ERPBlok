from anyblok import Declarations
from anyblok.column import String, Integer
from anyblok.relationship import Many2Many, Many2One

register = Declarations.register
Access = Declarations.Model.Access
Login = Declarations.Model.Web.Login


@register(Access)
class User:

    id = Integer(primary_key=True)
    first_name = String()
    last_name = String(nullable=False)
    login = Many2One(model=Login, nullable=False, unique=True)
    groups = Many2Many(model=Access.Group)
