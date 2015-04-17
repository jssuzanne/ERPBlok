from anyblok import Declarations
from lxml import etree, html


register = Declarations.register
Model = Declarations.Model
Mixin = Declarations.Mixin
Integer = Declarations.Column.Integer
Boolean = Declarations.Column.Boolean
Many2One = Declarations.RelationShip.Many2One
String = Declarations.Column.String
Selection = Declarations.Column.Selection


@register(Mixin)
class ViewType:

    mode = Selection(selections='get_mode_choices', nullable=False)

    @classmethod
    def get_mode_choices(cls):
        """ Return the View type available

        :rtype: dict(registry name: label)
        """
        return {
            'Model.UI.View.List': 'List view',
            'Model.UI.View.Form': 'Form view',
        }


@register(Model.UI)
class View(Mixin.ViewType):

    id = Integer(primary_key=True)
    selectable = Boolean(default=False)
    action = Many2One(model=Model.UI.Action, one2many='views', nullable=False)
    template = String(nullable=False)
    add_delete = Boolean(default=True)
    add_new = Boolean(default=True)
    add_edit = Boolean(default=True)

    def render(self):
        """ Return the View render"""
        return self.registry.get(self.mode)().render(self)

    @classmethod
    def render_from_scratch(cls, action):
        """ Make a render for List and Form view without template

        :param action: instance of the model UI.Action
        :rtype: list [selected view, [view(List / form) render])
        """
        _list = cls.registry.UI.View.List().render_from_scratch(action)
        _form = cls.registry.UI.View.Form().render_from_scratch(action)
        return _list['id'], [_list, _form]


@register(Mixin)  # noqa
class View:
    mode_name = None

    def render(self, view):
        Model = self.registry.get(view.action.model)
        pks = Model.get_primary_keys()
        return {
            'id': view.id,
            'selectable': view.selectable,
            'mode': self.mode_name,
            'primary_keys': pks,
        }

    def get_buttons(self, view):
        # FIXME Add models UI.View.Button
        # FIXME Add models UI.Action.Button
        return []

    def get_groups_buttons(self, view):
        # FIXME Add models UI.View.Button.Group
        # FIXME Add models UI.Action.Button.Group
        return []

    def get_transitions(self, view):
        return {x.name: (x.code, x.view.id)
                for x in view.action.transitions
                if x.mode == self.__registry_name__}


@register(Model.UI.View)
class List(Mixin.View):
    "List View"

    id = 1000001
    mode_name = 'List'

    def _rc_get_headers(self, fields, headers, node, level):
        maxlevel = level
        nbel = 0
        els = []
        ordered_fields = []
        if level not in headers:
            headers[level] = []
        for el in node.getchildren():
            if el.tag is etree.Comment:
                continue
            elif el.tag.lower() == 'group':
                subfields, submaxlevel, subnbel = self._rc_get_headers(
                    fields, headers, el, level + 1)
                if submaxlevel > maxlevel:
                    maxlevel = submaxlevel

                group = {
                    'label': el.attrib.get('label', ''),
                    'colspan': subnbel,
                }
                headers[level].append(group)
                els.append(group)
                ordered_fields.extend(subfields)
            elif el.tag.lower() == 'field':
                label = el.attrib.get('label')
                name = el.attrib.get('name')
                if not label:
                    label = fields[el.attrib.get('name')]['label']

                el = {
                    'id': name,
                    'label': label,
                    'colspan': 1,
                }
                headers[level].append(el)
                els.append(el)
                ordered_fields.append(name)

        for el in els:
            el['rowspan'] = maxlevel - level + 1

        return ordered_fields, maxlevel, nbel

    def get_button_delete(self):
        return {
            'label': 'Delete',
            'visibility': 'on-readonly on-selected',
            'fnct': 'delete_entry',
        }

    def get_button_new(self):
        return {
            'label': 'New',
            'visibility': 'on-readonly',
            'fnct': 'new_entry',
        }

    def get_buttons(self, view):
        res = super(List, self).get_buttons(view)
        if view.add_delete and view.action.add_delete:
            res.append(self.get_button_delete())

        if view.add_new and view.action.add_delete:
            res.append(self.get_button_new())

        return res

    def render(self, view):
        """ Specific render for a list view """
        res = super(List, self).render(view)
        tmpl = self.registry.erpblok_views.get_template(
            view.template, tostring=False)
        fields_name = [x.attrib.get('name') for x in tmpl.findall('.//field')]
        Model = self.registry.get(view.action.model)
        fields_description = Model.fields_description(fields=fields_name)
        headers = {}
        ordered_fields, level, _ = self._rc_get_headers(
            fields_description, headers, tmpl, 0)
        res.update({
            'fields': fields_name,
            'fields2display': [fields_description[x] for x in ordered_fields],
            'headers': list(headers.values()),
            'buttons': self.get_buttons(view),
            'buttons': self.get_buttons(view),
            'groups_buttons': self.get_groups_buttons(view),
            'transitions': self.get_transitions(view),
        })
        return res

    def render_from_scratch(self, action):
        """ Render without template for List view

        :param action: instance of the model UI.Action
        """
        Model = self.registry.get(action.model)
        fields = Model.fields_description()
        pks = Model.get_primary_keys()
        return {
            'id': self.id,  # arbitrary id
            'selectable': True,
            'mode': 'List',
            'primary_keys': pks,
            'fields': [x for x in fields.keys() if x not in pks],
            'fields2display': [x for y, x in fields.items() if y not in pks],
            'headers': [[x for y, x in fields.items() if y not in pks]],
            'checkbox': True,
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
                'selectRecord': ('open_view', self.registry.UI.View.Form.id),
                'newRecord': ('open_view', self.registry.UI.View.Form.id),
            },
        }


@register(Model.UI.View)
class Form(Mixin.View):
    "Form View"

    id = 1000002
    mode_name = 'Form'

    def get_template_replace_label(self, el, fields_description):
        el_for = el.attrib.get('for')
        if el_for in fields_description:
            el.text = fields_description[el_for]['label']

    def get_template_replace_field_attribute(self, k, v, field_description):
        if k == 'name':
            return
        elif k in ('type',):
            field_description[k] = v

    def get_template_replace_field(self, el, fields_description):
        el_name = el.attrib.get('name')
        if el_name in fields_description:
            div = etree.Element('div')
            div.set('id', el_name)
            for k, v in el.attrib.items():
                self.get_template_replace_field_attribute(
                    k, v, fields_description[el_name])

            return div

        return None

    def get_template_replace(self, tmpl, fields_description):
        for node in tmpl.getchildren():
            if node.tag is etree.Comment:
                continue
            else:
                tag = node.tag.lower()
                if hasattr(self, 'get_template_replace_' + tag):
                    el = getattr(self, 'get_template_replace_' + tag)(
                        node, fields_description)

                    if el is not None:
                        tmpl.replace(node, el)

                if node.getchildren():
                    self.get_template_replace(node, fields_description)

    def get_template(self, view):
        Model = self.registry.get(view.action.model)
        tmpl = self.registry.erpblok_views.get_template(
            view.template, tostring=False)
        tmpl.tag = 'div'
        fields_name = [x.attrib.get('name') for x in tmpl.findall('.//field')]
        fields_description = Model.fields_description(fields=fields_name)
        self.get_template_replace(tmpl, fields_description)
        tmpl = html.tostring(tmpl)
        return [self.registry.erpblok_views.decode(tmpl.decode('utf-8')),
                fields_name, fields_description]

    def get_button_edit(self):
        return {
            'label': 'Edit',
            'visibility': "on-readonly",
            'fnct': 'edit_view',
        }

    def get_button_save(self):
        return {
            'label': 'Save',
            'visibility': 'on-readwrite',
            'fnct': 'save_view',
        }

    def get_button_cancel(self):
        return {
            'label': 'Cancel',
            'visibility': 'on-readwrite',
            'fnct': 'read_view',
        }

    def get_button_new(self):
        return {
            'label': 'New',
            'visibility': '',
            'fnct': 'new_entry',
        }

    def get_button_delete(self):
        return {
            'label': 'Delete',
            'fnct': 'delete_entry',
        }

    def get_buttons(self, view):
        res = super(Form, self).get_buttons(view)
        add_save = False
        if view.add_edit and view.action.add_edit:
            res.append(self.get_button_edit())
            res.append(self.get_button_save())
            add_save = True
            res.append(self.get_button_cancel())

        if view.add_new and view.action.add_new and not add_save:
            res.append(self.get_button_save())

        return res

    def get_groups_buttons(self, view):
        res = super(Form, self).get_groups_buttons(view)

        def get_group_options():
            groups = [x for x in res if x['id'] == 'group-options']
            if groups:
                return groups[0]

            group = {
                'label': 'Options',
                'id': 'group-options',
                'visibility': 'on-readonly',
                'buttons': [],
            }
            res.append(group)
            return group

        if view.add_new and view.action.add_new:
            group = get_group_options()
            group['buttons'].append(self.get_button_new())

        if view.add_delete and view.action.add_delete:
            group = get_group_options()
            group['buttons'].append(self.get_button_delete())

        return res

    def render(self, view):
        """ Specific render for a list view """
        res = super(Form, self).render(view)
        template, fields_name, fields_description = self.get_template(view)
        res.update({
            'fields': fields_name,
            'template': template,
            'fields2display': [fields_description[x] for x in fields_name],
            'buttons': self.get_buttons(view),
            'groups_buttons': self.get_groups_buttons(view),
            'transitions': self.get_transitions(view),
        })
        return res

    def render_from_scratch(self, action):
        """ Render without template for Form view

        :param action: instance of the model UI.Action
        """
        Model = self.registry.get(action.model)
        root = etree.Element('div')
        fields = Model.fields_description()
        pks = Model.get_primary_keys()
        for name, value in fields.items():
            if name in pks:
                continue

            _label = etree.SubElement(root, 'label')
            _label.set('for', value['id'])
            _label.text = value['label']
            field = etree.SubElement(root, 'div')
            field.set('id', value['id'])

        return {
            'id': self.id,
            'mode': 'Form',
            'template': etree.tostring(root).decode('utf-8'),
            'primary_keys': pks,
            'fields': [x for x in fields.keys() if x not in pks],
            'fields2display': [x for y, x in fields.items() if y not in pks],
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
                            'label': 'New',
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
