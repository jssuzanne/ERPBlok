from anyblok import Declarations


register = Declarations.register
PyramidJsonRPC = Declarations.PyramidJsonRPC


@register(PyramidJsonRPC)
class View:

    @PyramidJsonRPC.rpc_method(request_method='POST')
    def get_entries(self, model=None, primary_keys=None, fields=None, **kwargs):
        res = [
            {'login': 'admin', 'password': 'admin'},
            {'login': 'riri', 'password': 'admin'},
            {'login': 'fifi', 'password': 'admin'},
            {'login': 'loulou', 'password': 'admin'},
        ]
        res.extend({'login': 'user %d' % x, 'password': 'password %d' % x}
                   for x in range(50))
        return res


PyramidJsonRPC.add_route(PyramidJsonRPC.View, '/web/client/view')
