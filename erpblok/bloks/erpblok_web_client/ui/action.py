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

    def render(self):
        views = []
        selected = self.selected

        if not self.views:
            selected, views = self.registry.UI.View.render_from_scratch(self)

        return {
            'model': self.model,
            'id': self.id,
            'label': self.label,
            'dialog': self.dialog,
            'views': views,
            'selected': selected,
        }
