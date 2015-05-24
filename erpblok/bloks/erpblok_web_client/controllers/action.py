from anyblok import Declarations


register = Declarations.register
PyramidJsonRPC = Declarations.PyramidJsonRPC

Sec = Declarations.SecurityManager

READ = Declarations.Permission.read

@register(PyramidJsonRPC)
class Action:

    @PyramidJsonRPC.rpc_method()
    def load(self, action=None, **kwargs):
        """ return the action render

        :param action: id of the action """
        UIAction = self.registry.UI.Action
        action = UIAction.query().filter(UIAction.id == int(action)).first()
        principals = pyramid_get_principals()
        if not Sec.check_permission(self, principals, READ):
            return 403 # ce qu'il faut
        return action.render()


PyramidJsonRPC.add_route(PyramidJsonRPC.Action, '/web/client/action')
