from anyblok import Declarations
from anyblok.column import Integer, String
from anyblok.relationship import Many2Many, Many2One

register = Declarations.register
UI = Declarations.Model.UI
Group = Declarations.Model.Access.Group
Space = Declarations.Model.Web.Space


@register(UI)
class Menu:

    id = Integer(primary_key=True)
    label = String(nullable=False)
    space = Many2One(model=Space, one2many='menus')
    parent = Many2One(model='Model.UI.Menu', one2many='children')
    order = Integer(nullable=False, default=100)
    action = Many2One(model=UI.Action, one2many="menus")
    groups = Many2Many(model=Group)
