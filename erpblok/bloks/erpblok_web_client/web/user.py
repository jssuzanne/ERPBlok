from anyblok import Declarations
from anyblok.column import String, Integer
from anyblok.relationship import Many2Many, One2One, Many2One

register = Declarations.register
Access = Declarations.Model.Access
Web = Declarations.Model.Web
Login = Declarations.Model.Web.Login
Space = Declarations.Model.Web.Space


@register(Web)
class User:

    id = Integer(primary_key=True)
    first_name = String()
    last_name = String(nullable=False)
    login = One2One(model=Login, nullable=False, backref="user")
    default_space = Many2One(model=Space, nullable=False)
    groups = Many2Many(model=Access.Group)

    def __str__(self):
        return '%s %s' % (self.first_name or '', self.last_name)

    def get_description(self):
        return {
            'label': str(self),
            'space': self.default_space and self.default_space.id,
        }

    def get_menus(self):
        res = [
            {
                'label': 'Other',
                'menus': [
                    {
                        'id': 'return_to_login_page',
                        'label': 'Log out',
                        'description': 'Close and return to the login page',
                    },
                ],
            },
        ]
        return res

    def has_groups(self, groups):
        Groups = self.registry.Access.Group
        User = self.registry.Web.User
        query = User.query().filter(User.groups.any(Groups.name.in_(groups)))
        if query.count():
            return True

        return False
