from anyblok import Declarations


register = Declarations.register
Access = Declarations.Model.Access
String = Declarations.Column.String


@register(Access)
class Group:

    name = String(primary_key=True)
    label = String(nullable=True)
