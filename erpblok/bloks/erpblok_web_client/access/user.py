from anyblok import Declarations
from anyblok.column import String, Integer
from anyblok.relationship import Many2Many, One2One

register = Declarations.register
Access = Declarations.Model.Access
Login = Declarations.Model.Web.Login


@register(Access)
class User:

    id = Integer(primary_key=True)
    first_name = String()
    last_name = String(nullable=False)
    login = One2One(model=Login, nullable=False, backref="user")
    groups = Many2Many(model=Access.Group)

    def __str__(self):
        return '%s %s' % (self.first_name or '', self.last_name)
