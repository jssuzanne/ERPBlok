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

    @classmethod
    def get_descriptions(cls, category):
        return [
            {
                'id': self.id,
                'label': self.label,
                'icon': self.icon,
                'description': self.description,
            }
            for self in cls.query().filter(cls.category == category).order_by(cls.order).all()
        ]


@Declarations.register(Declarations.Model.Web.Space)
class Category:

    id = Integer(primary_key=True)
    label = String(nullable=False)
    icon = String()
    order = Integer(nullable=False, default=100)
    groups = Many2Many(model=Declarations.Model.Access.Group)

    @classmethod
    def get_descriptions(cls):
        res = []
        for category in cls.query().order_by(cls.order).all():
            spaces = cls.registry.Web.Space.get_descriptions(category)
            if spaces:
                res.append({
                    'id': category.label,
                    'icon': category.icon,
                    'label': category.label,
                    'menus': spaces})

        return res
