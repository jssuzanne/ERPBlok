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
        res = {}
        System = cls.registry.System

        def get_query(Model):
            return Model.query().filter(Model.model == model).all()

        for col in get_query(System.Column):
            res[col.name] = {x: getattr(col, x)
                             for x in ('label', 'nullable')}
            res[col.name]['id'] = col.name
            res[col.name]['type'] = col.ctype

        for rs in get_query(System.RelationShip):
            res[rs.name] = {x: getattr(rs, x)
                            for x in ('label', 'nullable')}
            res[rs.name]['id'] = rs.name
            res[rs.name]['type'] = rs.rtype

        return res


@register(Model.UI.View)
class List(Mixin.View):

    id = 1000001

    @classmethod
    def render(cls, view):
        pass

    @classmethod
    def render_from_scratch(cls, action):
        Model = cls.registry.get(action.model)
        fields = cls.get_fields(action.model)
        return {
            'id': cls.id,  # arbitrary id
            'selectable': True,
            'mode': 'List',
            'primary_keys': Model.get_primary_keys(),
            'fields': list(fields.keys()),
            'fields2display': list(fields.values()),
            'headers': [list(fields.values())],
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
        for value in fields.values():
            _label = etree.SubElement(root, 'label')
            _label.set('for', value['id'])
            _label.text = value['label']
            field = etree.SubElement(root, 'div')
            field.set('id', value['id'])

        return {
            'id': cls.id,
            'mode': 'Form',
            'template': etree.tostring(root).decode('utf-8'),
            'primary_keys': Model.get_primary_keys(),
            'fields': list(fields.keys()),
        }
