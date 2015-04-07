from anyblok import Declarations
from lxml import etree


register = Declarations.register
Model = Declarations.Model
Mixin = Declarations.Mixin
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


@register(Mixin)  # noqa
class View:

    @classmethod
    def get_fields(cls, model):
        Column = cls.registry.System.Column
        RelationShip = cls.registry.System.RelationShip
        query = Column.query('name', 'label')
        query = query.filter(Column.model == model)
        query = query.filter(Column.primary_key.is_(False))
        columns = query.all()
        query = RelationShip.query('name', 'label')
        query = query.filter(RelationShip.model == model)
        relationships = query.all()
        return columns + relationships


@register(Model.UI.View)
class List(Mixin.View):

    id = 1000001

    @classmethod
    def render(cls, view):
        pass

    @classmethod
    def render_from_scratch(cls, action):
        Model = cls.registry.get(action.model)
        _fields = cls.get_fields(action.model)
        fields = [x[0] for x in _fields]
        return {
            'id': cls.id,  # arbitrary id
            'selectable': True,
            'mode': 'List',
            'primary_keys': Model.get_primary_keys(),
            'fields': fields,
            'fields2display': fields,
            'headers': [[{'id': x, 'label': y, 'colspan': 1, 'rowspan': 1}
                        for x, y in _fields]],
            'transitions': {
                'selectRecord': ('open_view', cls.registry.UI.View.Form.id),
            },
        }


@register(Model.UI.View)
class Form(Mixin.View):

    id = 1000002

    @classmethod
    def render(cls, view):
        pass

    @classmethod
    def render_from_scratch(cls, action):
        Model = cls.registry.get(action.model)
        root = etree.Element('div')
        fields = cls.get_fields(action.model)
        for name, label in fields:
            _label = etree.SubElement(root, 'label')
            _label.set('for', name)
            _label.text = label
            field = etree.SubElement(root, 'div')
            field.set('id', name)

        return {
            'id': cls.id,
            'mode': 'Form',
            'template': etree.tostring(root).decode('utf-8'),
            'primary_keys': Model.get_primary_keys(),
            'fields': [x[0] for x in fields],
        }
