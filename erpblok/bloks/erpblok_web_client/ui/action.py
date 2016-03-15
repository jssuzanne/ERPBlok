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

    def render(self, user):
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

            views = self.views.render(user)

        return {
            'model': self.model,
            'id': self.id,
            'label': self.label,
            'dialog': self.dialog,
            'views': views,
            'selected': selected,
            'add_edit': self.add_edit,
            'add_delete': self.add_delete,
            'add_new': self.add_new,
        }

    @classmethod
    def render_x2x_from_scratch(cls, model, user, **kwargs):
        # TODO change transition
        query = cls.query().filter_by(model=model)
        if query.count():
            res = query.first().render(user)
            view_type = kwargs.get('view_type',
                                   'Model.UI.View.Form').split('.')[-1]
            view = None
            for v in res['views']:
                if v['mode'] == view_type:
                    view = v

            res['views'] = [view]
            res['selected'] = view['id']
            return res

        action = cls(model=model)  # tempory action
        View = cls.registry.UI.View
        viewtype = kwargs.get('view_type', 'Model.UI.View.Form')
        query = View.query().join(cls, (cls.id == View.ui_action_id))
        query = query.filter(cls.model == model)
        query = query.filter(View.mode == viewtype)
        if query.count():
            view = query.first()
            view.action = action
            view = view.render(user)
            cls.registry.rollback()
        else:
            view = cls.registry.get(viewtype)().render_from_scratch(action)

        selected = view['id']
        return {
            'model': model,
            'label': kwargs.get('label', ''),
            'dialog': kwargs.get('dialog', False),
            'views': [view],
            'selected': selected,
            'add_edit': True,
            'add_delete': True,
            'add_new': True,
        }
