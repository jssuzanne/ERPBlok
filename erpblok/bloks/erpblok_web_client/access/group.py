from anyblok import Declarations
from anyblok.column import String

register = Declarations.register
Access = Declarations.Model.Access


@register(Access)
class Group:

    name = String(primary_key=True)
    label = String(nullable=True)
