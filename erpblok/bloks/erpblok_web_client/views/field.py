from pyramid_rpc.jsonrpc import jsonrpc_method
from pyramid.view import view_defaults
from anyblok_pyramid import current_blok


@view_defaults(installed_blok=current_blok())
class Field:

    def __init__(self, request):
        self.request = request
        self.registry = request.anyblok.registry

    @jsonrpc_method(endpoint='web_client_field')
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

    @jsonrpc_method(endpoint='web_client_field')
    def x2One_render(self, model=None, primary_keys=None):
        """ return the action render

        :param action: id of the action """
        Model = self.registry.get(model)
        entry = Model.from_primary_keys(**primary_keys)
        return entry.field_render()

    @jsonrpc_method(endpoint='web_client_field')
    def x2One_search(self, model=None, value=None):
        return self.registry.get(model).x2One_search(value)

    @jsonrpc_method(endpoint='web_client_field')
    def get_RelationShip_entries(self, model=None, display=None):
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
