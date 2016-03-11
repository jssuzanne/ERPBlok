from anyblok import Declarations


register = Declarations.register
PyramidJsonRPC = Declarations.PyramidJsonRPC


@register(PyramidJsonRPC)
class Action:

    @PyramidJsonRPC.rpc_method()
    def load(self, action=None, **kwargs):
        """ return the action render

        :param action: id of the action """
        user_id = self.request.session['user_id']
        user = self.registry.Web.User.query().get(user_id)
        UIAction = self.registry.UI.Action
        action = UIAction.query().filter(UIAction.id == int(action)).first()
        return action.render(user)


PyramidJsonRPC.add_route(PyramidJsonRPC.Action, '/web/client/action')
