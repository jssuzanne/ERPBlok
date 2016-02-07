from anyblok import Declarations
from anyblok.column import String, Boolean, Integer

register = Declarations.register
Model = Declarations.Model


@register(Model.UI)
class Action:

    id = Integer(primary_key=True)
    model = String(foreign_key=Model.System.Model.use('name'), nullable=False)
    label = String(nullable=False)
    dialog = Boolean(default=False)
    selected = Integer()
    add_delete = Boolean(default=True)
    add_new = Boolean(default=True)
    add_edit = Boolean(default=True)

    def render(self):
        """ Return the information of one action """
        selected = self.selected

        if not self.views:
            selected, views = self.registry.UI.View.render_from_scratch(self)
        else:
            if not selected:
                selectables = [(v.order, v.id)
                               for v in self.views
                               if v.selectable]
                selectables.sort()
                selected = self.selected = selectables[0][1]

            views = self.views.render()

        return {
            'model': self.model,
            'id': self.id,
            'label': self.label,
            'dialog': self.dialog,
            'views': views,
            'selected': selected,
        }

    @classmethod
    def render_from_scratch_x2M(cls, field):
        # FIXME
        # option of action from html
        # get view from html
        action = cls.action_from_description(field)
        selected, views = cls.registry.UI.View.render_from_scratch(action)
        return {
            'model': field['model'],
            'label': field['label'],
            'dialog': field.get('dialog', False),
            'views': views,
            'selected': selected,
        }

    @classmethod
    def action_from_description(cls, field):
        return cls(model=field['model'])

    @classmethod
    def render_from_scratch_selection(cls, field):
        # FIXME
        # option of action from html
        # get view from html
        # multi = True if field['type'] in ('One else False
        action = cls.action_from_description(field)
        if action:
            return action.id

        return None

    @classmethod
    def render_from_scratch_x2O(cls, field):
        # FIXME
        # option of action from html
        # get view from html
        # multi = True if field['type'] in ('One else False
        action = cls.action_from_description(field)
        View = cls.registry.UI.View
        query = View.query().join(cls, (cls.id == View.ui_action_id))
        query = query.filter(cls.model == field['model'])
        query = query.filter(View.mode == 'Model.UI.View.Form')
        if query.count():
            view = query.first().render()
        else:
            view = cls.registry.UI.View.Form().render_from_scratch(action)

        selected = view['id']
        return {
            'model': field['model'],
            'label': field['label'],
            'dialog': field.get('dialog', False),
            'views': [view],
            'selected': selected,
        }
