from anyblok import Declarations
from anyblok.column import Integer, String, Text
from anyblok.relationship import Many2One, Many2Many


@Declarations.register(Declarations.Model.Web)
class Space:

    id = Integer(primary_key=True)
    label = String(nullable=False)
    icon = String()
    description = Text()
    order = Integer(nullable=False, default=100)
    category = Many2One(model="Model.Web.Space.Category", nullable=False)
    groups = Many2Many(model=Declarations.Model.Access.Group)

    def get_description(self):
        return {
            'id': self.id,
            'label': self.label,
            'icon': self.icon,
        }


@Declarations.register(Declarations.Model.Web.Space)
class Category:

    id = Integer(primary_key=True)
    label = String(nullable=False)
    icon = String()
    order = Integer(nullable=False, default=100)
    groups = Many2Many(model=Declarations.Model.Access.Group)
