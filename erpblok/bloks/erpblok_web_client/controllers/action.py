from anyblok import Declarations


register = Declarations.register
PyramidJsonRPC = Declarations.PyramidJsonRPC


@register(PyramidJsonRPC)
class Action:

    @PyramidJsonRPC.rpc_method()
    def load(self, action=None, **kwargs):
        res = {
        }
        return res


PyramidJsonRPC.add_route(PyramidJsonRPC.Action, '/web/client/action')
