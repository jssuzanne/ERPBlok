from anyblok import Declarations
from sqlalchemy.sql import functions
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
        """ Return the View type available

        :rtype: dict(registry name: label)
        """
        # TODO use the declarations
        return {
            'Model.UI.View.List': 'List view',
            'Model.UI.View.Form': 'Form view',
        }

    def render(self):
        """ Return the View render"""
        return self.registry.get(self.mode).render(self)

    @classmethod
    def render_from_scratch(cls, action):
        """ Make a render for List and Form view without template

        :param action: instance of the model UI.Action
        :rtype: list [selected view, [view(List / form) render])
        """
        _list = cls.registry.UI.View.List.render_from_scratch(action)
        _form = cls.registry.UI.View.Form.render_from_scratch(action)
        return _list['id'], [_list, _form]


@register(Mixin)  # noqa
class View:

    @classmethod
    def get_fields(cls, model):
        Field = cls.registry.System.Field
        Column = cls.registry.System.Column
        RelationShip = cls.registry.System.RelationShip

        def get_query(Model):
            columns = [
                Model.name.label('id'),
                Model.label,
                Model.ftype.label('type'),
            ]
            if Model in (Column, RelationShip):
                columns.append(Model.nullable)
            else:
                columns.append(
                    functions.literal_column('true as nullable'))

            return Model.query(*columns).filter(Model.model == model)

        query = get_query(RelationShip).union_all(get_query(Column)).union_all(
            get_query(Field))
        return {x.id: {y: getattr(x, y)
                       for y in ('id', 'label', 'type', 'nullable')}
                for x in query.all()}


@register(Model.UI.View)
class List(Mixin.View):
    "List View"

    id = 1000001

    @classmethod
    def render(cls, view):
        """ Specific render for a list view """
        pass

    @classmethod
    def render_from_scratch(cls, action):
        """ Render without template for List view

        :param action: instance of the model UI.Action
        """
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
            'buttons': [
                {
                    'label': 'New',
                    'visibility': 'on-readonly',
                    'fnct': 'new_entry',
                },
                {
                    'label': 'Delete',
                    'visibility': 'on-readonly on-selected',
                    'fnct': 'delete_entry',
                },
            ],
            'transitions': {
                'selectRecord': ('open_view', cls.registry.UI.View.Form.id),
            },
        }


@register(Model.UI.View)
class Form(Mixin.View):
    "Form View"

    id = 1000002

    @classmethod
    def render(cls, view):
        """ Specific render for a Form view """
        pass

    @classmethod
    def render_from_scratch(cls, action):
        """ Render without template for Form view

        :param action: instance of the model UI.Action
        """
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
            'fields2display': list(fields.values()),
            'buttons': [
                {
                    'label': 'Edit',
                    'visibility': "on-readonly",
                    'fnct': 'edit_view',
                },
                {
                    'label': 'Save',
                    'visibility': 'on-readwrite',
                    'fnct': 'save_view',
                },
                {
                    'label': 'Close',
                    'visibility': "on-readonly",
                    'fnct': 'close_view',
                },
                {
                    'label': 'Cancel',
                    'visibility': 'on-readwrite',
                    'fnct': 'read_view',
                },
            ],
            'groups_buttons': [
                {
                    'label': 'Options',
                    'id': 'group-options',
                    'visibility': 'on-readonly',
                    'buttons': [
                        {
                            'label': 'Create',
                            'visibility': '',
                            'fnct': 'new_entry',
                        },
                        {
                            'label': 'Delete',
                            'fnct': 'delete_entry',
                        },
                    ],
                },
            ],
        }
