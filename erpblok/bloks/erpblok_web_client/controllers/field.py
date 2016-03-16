from anyblok import Declarations


register = Declarations.register
PyramidJsonRPC = Declarations.PyramidJsonRPC


@register(PyramidJsonRPC)
class Field:

    @PyramidJsonRPC.rpc_method()
    def get_action_for(self, action=None, model=None, view_type=None,
                       **kwargs):
        user_id = self.request.session['user_id']
        user = self.registry.Web.User.query().get(user_id)
        UIAction = self.registry.UI.Action
        if action:
            if isinstance(action, str):
                if model:
                    action = self.registry.IO.Mapping(model, action)
                # else raise
            else:
                action = UIAction.query().get(int(action))

            res = action.render(user)
            view_type = view_type.split('.')[-1]
            view = None
            for v in res['views']:
                if v['mode'] == view_type:
                    view = v

            res['views'] = [view]
            res['selected'] = view['id']
            return res
        else:
            return UIAction.render_x2x_from_scratch(
                model, user, view_type=view_type, **kwargs)

    @PyramidJsonRPC.rpc_method()
    def x2One_render(self, model=None, primary_keys=None, **kwargs):
        """ return the action render

        :param action: id of the action """
        Model = self.registry.get(model)
        entry = Model.from_primary_keys(**primary_keys)
        return entry.field_render()

    @PyramidJsonRPC.rpc_method()
    def x2One_search(self, model=None, value=None, **kwargs):
        return self.registry.get(model).x2One_search(value)

    @PyramidJsonRPC.rpc_method(request_method='POST')
    def get_RelationShip_entries(self, model=None, display=None, **kwargs):
        Model = self.registry.get(model)
        entries = []
        for m in Model.query().all():
            if display:
                pks = m.to_primary_keys()
                val = getattr(m, display)
                # TODO check if callable
                entries.append((pks, val))
            else:
                entries.append(m.field_render())

        return entries


PyramidJsonRPC.add_route(PyramidJsonRPC.Field, '/web/client/field')
