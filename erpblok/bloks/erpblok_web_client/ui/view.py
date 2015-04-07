from anyblok import Declarations


register = Declarations.register
Model = Declarations.Model
Integer = Declarations.Column.Integer
Boolean = Declarations.Column.Boolean
Selection = Declarations.Column.Selection
Many2One = Declarations.RelationShip.Many2One
String = Declarations.Column.String


@register(Model.UI)
class View:

    id = Integer(primary_key=True)
    selectable = Boolean(default=False)
    mode = Selection(selections='get_mode_choices', nullable=False)
    action = Many2One(model=Model.UI.Action, one2many='views', nullable=False)
    template = String(nullable=False)

    @classmethod
    def get_mode_choices(cls):
        # TODO use the declarations
        return {
            'Model.UI.View.List': 'List view',
            'Model.UI.View.Form': 'Form view',
        }

    def render(self):
        return self.registry.get(self.mode).render(self)

    @classmethod
    def render_from_scratch(cls, action):
        _list = cls.registry.UI.View.List.render_from_scratch(action)
        _form = cls.registry.UI.View.Form.render_from_scratch(action)
        return _list['id'], [_list, _form]


@register(Model.UI.View)
class List:

    id = 1000001

    @classmethod
    def render(cls, view):
        pass

    @classmethod
    def render_from_scratch(cls, action):
        Model = cls.registry.get(action.model)
        Column = cls.registry.System.Column
        query = Column.query('name', 'label')
        query = query.filter(Column.model == action.model)
        query = query.filter(Column.primary_key.is_(False))
        columns = query.all()
        fields = [x[0] for x in columns]
        return {
            'id': cls.id,  # arbitrary id
            'selectable': True,
            'mode': 'List',
            'primary_keys': Model.get_primary_keys(),
            'fields': fields,
            'fields2display': fields,
            'headers': [[{'id': x, 'label': y, 'colspan': 1, 'rowspan': 1}
                        for x, y in columns]],
            'transitions': {
                'selectRecord': ('open_view', cls.registry.UI.View.Form.id),
            },
        }


@register(Model.UI.View)
class Form:

    id = 1000002

    @classmethod
    def render(cls, view):
        pass

    @classmethod
    def render_from_scratch(cls, action):
        form = """
            <div>
                <label for="login">Login</label>
                <div id="login"></div>
                <label for="password">Password</label>
                <div id="password"></div>
            </div>
        """
        return {
            'id': cls.id,
            'mode': 'Form',
            'template': form,
            'primary_keys': ['login'],
            'fields': ['login', 'password'],
        }
