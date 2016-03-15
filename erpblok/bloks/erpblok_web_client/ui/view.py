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

    def render(self, user):
        """ Return the View render"""
        return self.registry.get(self.mode)().render(self, user)

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

    def render(self, view, user):
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


@register(Mixin)
class ViewAccessGroups:

    def get_unwanted_elements_for(self, tmpl, attribute, user):
        els = tmpl.findall(".//*[@%s]" % attribute)
        res = []
        for el in els:
            groups = [x.strip() for x in el.attrib[attribute].split(',') if x]
            if not user.has_groups(groups):
                res.append(el)

        return res

    def visible_only_for_access_group(self, tmpl, user):
        els = self.get_unwanted_elements_for(
            tmpl, 'visible-only-for-groups', user)
        for el in els:
            el.getparent().remove(el)

    def writable_only_for_access_group(self, tmpl, user):
        els = self.get_unwanted_elements_for(
            tmpl, 'writable-only-for-groups', user)
        for el in els:
            el.set('readonly', "1")


@register(Mixin)
class ViewRenderTemplate(Mixin.ViewAccessGroups):

    def get_template_replace_label(self, tmpl, fields_description):
        labels = tmpl.findall('.//label')
        for el in labels:
            el_for = el.attrib.get('for')
            for field in fields_description:
                if field['field_name'] == el_for:
                    if not el.text:
                        el.text = field['label']

    def get_fields_description(self, view, tmpl):
        fields = tmpl.findall('.//field')
        Model = self.registry.get(view.action.model)
        fields_description = Model.fields_description()
        fdesc = []
        counter = 0
        for el in fields:
            counter += 1
            name = el.attrib['name']
            field = fields_description[name].copy()
            fdesc.append(field)
            field['field_name'] = field['id']
            field['id'] += '-%d' % counter
            for k, v in el.attrib.items():
                if k not in ('field_name', 'id'):
                    field[k] = v

            for attr in ('type', 'writable-only-if', 'not-nullable-only-if',
                         'not-nullable-only-if'):
                if el.attrib.get(attr):
                    del el.attrib[attr]

            el.set('id', field['id'])
            if 'readonly' in field and isinstance(field['readonly'], str):
                if field['readonly'].lower() in ('true', '1'):
                    field['readonly'] = True
                else:
                    field['readonly'] = False
            for x in ('writable-only-if', 'not-nullable-only-if'):
                if x in field and field[x]:
                    field[x] = [field[x]]
                else:
                    field[x] = []

        return fdesc

    def update_interface_attributes(self, tmpl, fields_description):
        for el in tmpl.findall('.//*[@visible-only-if]'):
            class_attr = el.attrib.get(
                'class', '') + ' visibility-conditional-ui'
            el.set('class', class_attr)

        for attr in ('writable-only-if', 'not-nullable-only-if'):
            for el in tmpl.findall('.//*[@%s]' % attr):
                attr_val = el.attrib[attr]
                if attr_val:
                    for field in el.findall('.//field'):
                        field_id = field.attrib.get('id')
                        for fd in fields_description:
                            if fd['id'] == field_id:
                                fd[attr].append(attr_val)

        for field in fields_description:
            for attr in ('writable-only-if', 'not-nullable-only-if'):
                if attr in field:
                    field[attr] = ' || '.join(field[attr])

    def get_template(self, view, user):
        tmpl = self.registry.erpblok_views.get_template(
            view.template, tostring=False)
        self.visible_only_for_access_group(tmpl, user)
        self.writable_only_for_access_group(tmpl, user)
        tmpl.tag = 'div'
        fields_description = self.get_fields_description(view, tmpl)
        self.get_template_replace_label(tmpl, fields_description)
        self.update_interface_attributes(tmpl, fields_description)
        tmpl = html.tostring(tmpl)
        return [self.registry.erpblok_views.decode(tmpl.decode('utf-8')),
                fields_description]

    def render_template(self, view, user):
        """ Specific render for a list view """
        template, fields_description = self.get_template(view, user)
        return {
            'fields': [x['field_name'] for x in fields_description],
            'template': template,
            'fields2display': fields_description,
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
class List(Mixin.ViewMultiEntries, Mixin.ViewAccessGroups):
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

    def get_tmpl_attribute_format_bool(self, tmpl, key, default=False):
        value = tmpl.attrib.get(key, str(default))
        if value.lower() in ('true', '1'):
            return True
        else:
            return False

    def render(self, view, user):
        """ Specific render for a list view """
        res = super(List, self).render(view, user)
        tmpl = self.registry.erpblok_views.get_template(
            view.template, tostring=False)
        self.visible_only_for_access_group(tmpl, user)
        self.writable_only_for_access_group(tmpl, user)
        fields_name = [x.attrib.get('name') for x in tmpl.findall('.//field')]
        checkbox = self.get_tmpl_attribute_format_bool(tmpl, 'checkbox', True)
        inline = self.get_tmpl_attribute_format_bool(tmpl, 'inline', False)
        Model = self.registry.get(view.action.model)
        fields_description = deepcopy(Model.fields_description(
            fields=fields_name))
        headers = {}
        ordered_fields, level, _ = self._rc_get_headers(
            fields_description, headers, tmpl, 0)
        res.update({
            'fields': fields_name,
            'checkbox': checkbox,
            'inline': inline,
            'fields2display': ordered_fields,
            'headers': list(headers.values()),
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
        fields = []
        pks = Model.get_primary_keys()
        counter = 0
        headers = []
        fields_name = self.registry.System.Column.query().filter_by(
            model=action.model).all().name
        for field_name, field in Model.fields_description(fields_name).items():
            if field_name in pks:
                continue

            f = field.copy()
            f['field_name'] = field_name
            counter += 1
            f['id'] += '-%d' % counter
            fields.append(f)
            headers.append({
                'id': f['field_name'],
                'label': f['label'],
                'colspan': 1,
                'rowspan': 1,
            })

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
            'fields': [x['field_name'] for x in fields],
            'fields2display': fields,
            'headers': [headers],
            'checkbox': True,
            'buttons': buttons,
            'groups_buttons': [],
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

    def render(self, view, user):
        """ Specific render for a list view """
        res = super(Form, self).render(view, user)
        res.update(self.render_template(view, user))
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
        fields_name = self.registry.System.Column.query().filter_by(
            model=action.model).all().name
        fields = Model.fields_description(fields_name)
        pks = Model.get_primary_keys()
        fields_description = []
        counter = 0
        for name, value in fields.items():
            if name in pks:
                continue

            counter += 1
            f = fields[name].copy()
            f['field_name'] = f['id']
            f_id = f['id'] + '-%d' % counter
            f['id'] = f_id
            _label = etree.SubElement(root, 'label')
            _label.set('for', name)
            _label.text = value['label']
            field = etree.SubElement(root, 'field')
            field.set('name', name)
            field.set('id', f_id)
            fields_description.append(f)

        self.get_template_replace_label(root, fields_description)

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
            'fields': [x['field_name'] for x in fields_description],
            'fields2display': fields_description,
            'buttons': buttons,
            'groups_buttons': groups_buttons,
        }


@register(Model.UI.View)
class Thumbnails(Mixin.ViewMultiEntries, Mixin.ViewRenderTemplate):
    "Form View"

    id = 1000002
    mode_name = 'Thumbnails'

    def render(self, view, user):
        """ Specific render for a list view """
        res = super(Thumbnails, self).render(view, user)
        res.update(self.render_template(view, user))
        res.update({
            'buttons': self.get_buttons(view),
            'groups_buttons': self.get_groups_buttons(view),
            'transitions': self.get_transitions(view),
        })
        return res
