from anyblok import Declarations


register = Declarations.register
Model = Declarations.Model
Mixin = Declarations.Mixin
Integer = Declarations.Column.Integer
Many2One = Declarations.RelationShip.Many2One
String = Declarations.Column.String
Selection = Declarations.Column.Selection


@register(Model.UI.Action)
class Transition(Mixin.ViewType):

    id = Integer(primary_key=True)
    name = String(nullable=False)
    action = Many2One(model=Model.UI.Action, one2many='transitions',
                      nullable=False)
    view = Many2One(model=Model.UI.View, nullable=False)
    code = Selection(selections='get_code_choices', nullable=False)

    @classmethod
    def get_code_choices(cls):
        """ Return the View type available

        :rtype: dict(registry name: label)
        """
        return {
            'open_view': 'Open view',
        }
