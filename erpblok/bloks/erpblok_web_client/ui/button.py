from anyblok import Declarations


register = Declarations.register
Model = Declarations.Model
Mixin = Declarations.Mixin
Integer = Declarations.Column.Integer
Many2One = Declarations.RelationShip.Many2One
String = Declarations.Column.String
Boolean = Declarations.Column.Boolean
Json = Declarations.Column.Json


@register(Model.UI.Action)
class Button(Mixin.ViewType):

    id = Integer(primary_key=True)
    label = String(nullable=False)
    on_readonly = Boolean(default=False)
    on_readwrite = Boolean(default=False)
    on_selected = Boolean(default=False)
    action = Many2One(model=Model.UI.Action, one2many='buttons',
                      nullable=False)
    function = String(nullable=False)
    method = String()

    @classmethod
    def get_mode_choices(cls):
        res = super(Button, cls).get_mode_choices()
        res['all'] = 'All'
        return res

    @classmethod
    def get_code_choices(cls):
        """ Return the View type available

        :rtype: dict(registry name: label)
        """
        return {
            'open_view': 'Open view',
        }

    def render_visibility(self):
        visibility = []
        if self.on_readonly:
            visibility.append('on-readonly')

        if self.on_readwrite:
            visibility.append('on-readwrite')

        if self.on_selected:
            visibility.append('on-selected')

        return ' '.join(visibility)

    def render(self, withoutgroup=True):
        res = {
            'label': self.label,
            'fnct': self.function,
            'visibility': self.render_visibility(),
            'method': self.method,
        }
        if withoutgroup:
            return res

        res.update({})
        return res
