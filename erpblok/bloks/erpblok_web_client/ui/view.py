from anyblok import Declarations
from anyblok.column import Integer, Boolean, String, Selection
from anyblok.relationship import Many2One
from lxml import etree, html
from copy import deepcopy


register = Declarations.register
Model = Declarations.Model
Mixin = Declarations.Mixin


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
            'Model.UI.View.Thumbnails': 'Thumbnails view',
            'Model.UI.View.Form': 'Form view',
        }


@register(Model.UI)
class View(Mixin.ViewType):

    id = Integer(primary_key=True)
    order = Integer(sequence='ui__view_order_seq', nullable=False)
    selectable = Boolean(default=False)
    action = Many2One(model=Model.UI.Action, one2many='views', nullable=False)
    template = String(nullable=False)
    add_delete = Boolean(default=True)
    add_new = Boolean(default=True)
    add_edit = Boolean(default=True)
    is_selectable = Boolean(default=True)  # Only for multi

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
        res = []
        for button in view.action.buttons:
            if button.mode not in ('all', self.__registry_name__):
                continue

            if not button.group:
                res.append(button.render())

        return res

    def get_groups_buttons(self, view):
        groups = {}
        for button in view.action.buttons:
            if button.mode not in ('all', self.__registry_name__):
                continue

            if button.group:
                if button.group.label not in groups:
                    groups[button.group.label] = button.group.render()

                groups[button.group.label]['buttons'].append(
                    button.render())

        return list(groups.values())

    def get_transitions(self, view):
        return {x.name: (x.code, x.view.id)
                for x in view.action.transitions
                if x.mode == self.__registry_name__}

    def update_relation_ship_description(self, descriptions):
        # FIXME check external id
        Action = self.registry.UI.Action
        x2M = ('One2Many', 'Many2Many')
        for field in descriptions.values():
            if field['type'] in x2M:
                if not field.get('action'):
                    field['action'] = Action.render_from_scratch_x2M(field)
            if field['model']:
                if not field.get('action'):
                    field['action'] = Action.render_from_scratch_x2O(field)

                if not field.get('selection_action'):
                    field['selection_action'] = \
                        Action.render_from_scratch_selection(field)


@register(Mixin)
class ViewRenderTemplate:

    def get_template_replace_label(self, el, fields_description):
        el_for = el.attrib.get('for')
        if el_for in fields_description:
            el.text = fields_description[el_for]['label']

    def get_template_replace_field_attribute(self, k, v, field_description):
        if k == 'name':
            return
        elif k not in ('id', 'model', 'primary_key'):
            field_description[k] = v

    def get_template_replace_field(self, el, fields_description):
        el_name = el.attrib.get('name')
        if el_name in fields_description:
            div = etree.Element('div')
            div.set('id', el_name)
            _class = ["field"]
            for k, v in el.attrib.items():
                self.get_template_replace_field_attribute(
                    k, v, fields_description[el_name])
                if k not in ('type', 'class'):
                    div.set(k, v)

                if k == "class":
                    _class.extend(v.split(' '))

            div.set('class', ' '.join(_class))
            return div

        return None

    def get_template_replace_expr(self, el, fields_description):

        def replace(attrib, head, tail, notailifnextin=None):
            if notailifnextin is None:
                notailifnextin = []

            el.tag = 'div'
            del el.attrib[attrib]
            index = el.getparent().getchildren().index(el)
            if index == 0:
                el.getparent().text += head
            else:
                if el.getparent().getchildren()[index - 1].tail:
                    el.getparent().getchildren()[index - 1].tail += head
                else:
                    el.getparent().getchildren()[index - 1].tail = head

            if index != (len(el.getparent().getchildren()) - 1):
                nextel = el.getparent().getchildren()[index + 1]
                if nextel.tag == 'expr':
                    for expr in notailifnextin:
                        if expr in nextel.attrib.keys():
                            return

            if el.tail:
                el.tail = tail + el.tail
            else:
                el.tail = tail

        endop = '{{/if}}'

        for k, v in el.attrib.items():
            if k == "if":
                head = '{{if %(expr)s }}' % dict(expr=v)
                replace(k, head, endop, notailifnextin=('else', 'elif'))

            elif k == "else":
                head = '{{else}}'
                replace(k, head, endop)
            elif k == "elif":
                head = '{{else %(expr)s }}' % dict(expr=v)
                replace(k, head, endop, notailifnextin=('else', 'elif'))

    def get_template_replace(self, tmpl, fields_description):
        for node in tmpl.getchildren():
            if node.tag is etree.Comment:
                continue
            else:
                if node.getchildren():
                    self.get_template_replace(node, fields_description)

                tag = node.tag.lower()
                if hasattr(self, 'get_template_replace_' + tag):
                    el = getattr(self, 'get_template_replace_' + tag)(
                        node, fields_description)

                    if el is not None:
                        tmpl.replace(node, el)

    def get_template(self, view):
        Model = self.registry.get(view.action.model)
        tmpl = self.registry.erpblok_views.get_template(
            view.template, tostring=False)
        tmpl.tag = 'div'
        fields_name = [x.attrib.get('name') for x in tmpl.findall('.//field')]
        fields_description = deepcopy(Model.fields_description(
            fields=fields_name))
        self.get_template_replace(tmpl, fields_description)
        tmpl = html.tostring(tmpl)
        self.update_relation_ship_description(fields_description)
        return [self.registry.erpblok_views.decode(tmpl.decode('utf-8')),
                fields_name, fields_description]

    def render_template(self, view):
        """ Specific render for a list view """
        template, fields_name, fields_description = self.get_template(view)
        return {
            'fields': fields_name,
            'template': template,
            'fields2display': [fields_description[x] for x in fields_name],
        }


@register(Mixin)
class ViewMultiEntries(Mixin.View):

    def get_button_delete(self):
        return {
            'label': 'Delete',
            'visibility': 'on-readonly on-selected',
            'fnct': 'delete_entry',
            'method': '',
        }

    def get_button_new(self):
        return {
            'label': 'New',
            'visibility': 'on-readonly',
            'fnct': 'new_entry',
            'method': '',
        }

    def get_buttons(self, view):
        res = super(ViewMultiEntries, self).get_buttons(view)
        if view.add_delete and view.action.add_delete:
            res.append(self.get_button_delete())

        if view.add_new and view.action.add_delete:
            res.append(self.get_button_new())

        return res


@register(Model.UI.View)
class List(Mixin.ViewMultiEntries):
    "List View"

    id = 1000001
    mode_name = 'List'

    def _rc_get_headers_parent_options(self, el, parent_options):
        options = parent_options.copy()
        for k in ('readonly', 'nullable'):
            if k in el.attrib:
                options[k] = self.attrib[k]

        return options

    def _rc_get_headers_get_field(self, fields, name, el, options, counter):
        field = fields[name].copy()
        field.update(options)
        field.update({x: y for x, y in el.attrib.items()
                      if x not in ('label', 'name', 'colspan',
                                   'rowspan')})
        field['field_name'] = field['id']
        field['id'] += '-%d' % counter
        return field

    def _rc_get_headers(self, fields, headers, node, level, options=None,
                        counter=0):
        if options is None:
            options = {}

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
                    fields, headers, el, level + 1,
                    options=self._rc_get_headers_parent_options(el, options),
                    counter=counter)
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

                _el = {
                    'id': name,
                    'label': label,
                    'colspan': 1,
                }
                headers[level].append(_el)
                els.append(_el)
                counter += 1
                field = self._rc_get_headers_get_field(
                    fields, name, el, options, counter)
                ordered_fields.append(field)

        for el in els:
            el['rowspan'] = maxlevel - level + 1

        return ordered_fields, maxlevel, nbel

    def render(self, view):
        """ Specific render for a list view """
        res = super(List, self).render(view)
        tmpl = self.registry.erpblok_views.get_template(
            view.template, tostring=False)
        fields_name = [x.attrib.get('name') for x in tmpl.findall('.//field')]
        Model = self.registry.get(view.action.model)
        fields_description = deepcopy(Model.fields_description(
            fields=fields_name))
        headers = {}
        ordered_fields, level, _ = self._rc_get_headers(
            fields_description, headers, tmpl, 0)
        self.update_relation_ship_description(fields_description)
        res.update({
            'fields': fields_name,
            'checkbox': view.is_selectable,
            'fields2display': ordered_fields,
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
        fields = deepcopy(Model.fields_description())
        self.update_relation_ship_description(fields)
        pks = Model.get_primary_keys()
        buttons = []
        if action.add_new:
            buttons.append(self.get_button_new())

        if action.add_delete:
            buttons.append(self.get_button_delete())

        return {
            'id': self.id,  # arbitrary id
            'selectable': True,
            'mode': 'List',
            'primary_keys': pks,
            'fields': [x for x in fields.keys() if x not in pks],
            'fields2display': [x for y, x in fields.items() if y not in pks],
            'headers': [[x for y, x in fields.items() if y not in pks]],
            'checkbox': True,
            'buttons': buttons,
            'transitions': {
                'selectRecord': ('open_view', self.registry.UI.View.Form.id),
                'newRecord': ('open_view', self.registry.UI.View.Form.id),
            },
        }


@register(Model.UI.View)
class Form(Mixin.View, Mixin.ViewRenderTemplate):
    "Form View"

    id = 1000002
    mode_name = 'Form'

    def get_button_edit(self):
        return {
            'label': 'Edit',
            'visibility': "on-readonly",
            'fnct': 'edit_view',
            'method': '',
        }

    def get_button_save(self):
        return {
            'label': 'Save',
            'visibility': 'on-readwrite',
            'fnct': 'save_view',
            'method': '',
        }

    def get_button_cancel(self):
        return {
            'label': 'Cancel',
            'visibility': 'on-readwrite',
            'fnct': 'read_view',
            'method': '',
        }

    def get_button_new(self):
        return {
            'label': 'New',
            'visibility': '',
            'fnct': 'new_entry',
            'method': '',
        }

    def get_button_close(self):
        return {
            'label': 'Close',
            'visibility': "on-readonly",
            'fnct': 'close_view',
            'method': '',
        }

    def get_button_delete(self):
        return {
            'label': 'Delete',
            'fnct': 'delete_entry',
            'method': '',
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

        if view.id != view.action.selected:
            res.append(self.get_button_close())

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
        res.update(self.render_template(view))
        res.update({
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
            _label.set('for', name)
            _label.text = value['label']
            field = etree.SubElement(root, 'field')
            field.set('name', name)

        self.get_template_replace(root, fields)

        buttons = []
        groups_buttons = []
        new = self.get_button_new()
        edit = self.get_button_edit()
        save = self.get_button_save()
        cancel = self.get_button_cancel()
        close = self.get_button_close()
        if action.add_new and action.add_edit:
            buttons.append(edit)
            buttons.append(save)
            buttons.append(close)
            buttons.append(cancel)
            groups_buttons.append(new)
        elif action.add_new:
            buttons.append(save)
            buttons.append(close)
            buttons.append(cancel)
            groups_buttons.append(new)
        elif action.add_edit:
            buttons.append(edit)
            buttons.append(save)
            buttons.append(close)
            buttons.append(cancel)

        if action.add_delete:
            groups_buttons.append(self.get_button_delete())

        if groups_buttons:
            groups_buttons = [
                {
                    'label': 'Options',
                    'id': 'group-options',
                    'visibility': 'on-readonly',
                    'buttons': groups_buttons,
                }
            ]

        return {
            'id': self.id,
            'mode': 'Form',
            'template': self.registry.erpblok_views.decode(
                html.tostring(root).decode('utf-8')),
            'primary_keys': pks,
            'fields': [x for x in fields.keys() if x not in pks],
            'fields2display': [x for y, x in fields.items() if y not in pks],
            'buttons': buttons,
            'groups_buttons': groups_buttons,
        }


@register(Model.UI.View)
class Thumbnails(Mixin.ViewMultiEntries, Mixin.ViewRenderTemplate):
    "Form View"

    id = 1000002
    mode_name = 'Thumbnails'

    def render(self, view):
        """ Specific render for a list view """
        res = super(Thumbnails, self).render(view)
        res.update(self.render_template(view))
        res.update({
            'buttons': self.get_buttons(view),
            'groups_buttons': self.get_groups_buttons(view),
            'transitions': self.get_transitions(view),
        })
        return res
