from anyblok import Declarations


register = Declarations.register
PyramidJsonRPC = Declarations.PyramidJsonRPC


@register(PyramidJsonRPC)
class Action:

    @PyramidJsonRPC.rpc_method()
    def load(self, action=None, **kwargs):
        UIAction = register.Model.UI.Action
        action = UIAction.query().filter(UIAction.id == int(action)).first()
        return action.render()


PyramidJsonRPC.add_route(PyramidJsonRPC.Action, '/web/client/action')
