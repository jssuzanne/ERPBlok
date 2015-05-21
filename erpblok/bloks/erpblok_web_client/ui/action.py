from anyblok import Declarations


register = Declarations.register
Model = Declarations.Model
Integer = Declarations.Column.Integer
Boolean = Declarations.Column.Boolean
String = Declarations.Column.String


@register(Model.UI)
class Action:

    id = Integer(primary_key=True)
    model = String(foreign_key=(Model.System.Model, 'name'), nullable=False)
    label = String(nullable=False)
    dialog = Boolean(default=False)
    selected = Integer()
    add_delete = Boolean(default=True)
    add_new = Boolean(default=True)
    add_edit = Boolean(default=True)

    def render(self):
        """ Return the information of one action """
        selected = self.selected

        if not self.views:
            selected, views = self.registry.UI.View.render_from_scratch(self)
        else:
            if not selected:
                selectables = [(v.order, v.id)
                               for v in self.views
                               if v.selectable]
                selectables.sort()
                selected = self.selected = selectables[0][1]

            views = self.views.render()

        return {
            'model': self.model,
            'id': self.id,
            'label': self.label,
            'dialog': self.dialog,
            'views': views,
            'selected': selected,
        }

    @classmethod
    def render_from_scratch(cls, field):
        action = cls(model=field['model'])
        selected, views = cls.registry.UI.View.render_from_scratch(action)
        return {
            'model': field['model'],
            'label': field['label'],
            'dialog': field.get('dialog', False),
            'views': views,
            'selected': selected,
        }
