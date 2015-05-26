from anyblok import Declarations
from anyblok.column import String, Boolean, Integer
from anyblok.relationship import Many2One

register = Declarations.register
Model = Declarations.Model
Mixin = Declarations.Mixin


@register(Mixin)
class UIButton:
    label = String(nullable=False)
    on_readonly = Boolean(default=False)
    on_readwrite = Boolean(default=False)
    on_selected = Boolean(default=False)

    def render_visibility(self):
        visibility = []
        if self.on_readonly:
            visibility.append('on-readonly')

        if self.on_readwrite:
            visibility.append('on-readwrite')

        if self.on_selected:
            visibility.append('on-selected')

        return ' '.join(visibility)


@register(Model.UI.Action)
class ButtonGroup(Mixin.UIButton):

    code = String(primary_key=True)

    def render(self):
        return {
            'label': self.label,
            'id': self.code,
            'visibility': self.render_visibility(),
            'buttons': [],
        }


@register(Model.UI.Action)
class Button(Mixin.UIButton, Mixin.ViewType):

    id = Integer(primary_key=True)
    action = Many2One(model=Model.UI.Action, one2many='buttons',
                      nullable=False)
    group = Many2One(model=Model.UI.Action.ButtonGroup)
    function = String(nullable=False)
    method = String()

    @classmethod
    def get_mode_choices(cls):
        res = super(Button, cls).get_mode_choices()
        res['all'] = 'All'
        return res

    def render(self):
        return {
            'label': self.label,
            'fnct': self.function,
            'visibility': self.render_visibility(),
            'method': self.method,
        }
