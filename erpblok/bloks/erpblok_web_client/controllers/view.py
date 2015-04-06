from anyblok import Declarations


register = Declarations.register
PyramidJsonRPC = Declarations.PyramidJsonRPC


@register(PyramidJsonRPC)
class View:

    def mock(self):
        res = [
            {'login': 'admin', 'password': 'admin'},
            {'login': 'riri', 'password': 'admin'},
            {'login': 'fifi', 'password': 'admin'},
            {'login': 'loulou', 'password': 'admin'},
        ]
        res.extend({'login': 'user %d' % x, 'password': 'password %d' % x}
                   for x in range(50))
        return res

    @PyramidJsonRPC.rpc_method(request_method='POST')
    def get_entries(self, model=None, primary_keys=None, fields=None, **kwargs):
        return self.mock()

    @PyramidJsonRPC.rpc_method(request_method='POST')
    def get_entry(self, model=None, primary_keys=None, fields=None, **kwargs):
        mock = self.mock()
        for k, v in primary_keys.items():
            mock = [x for x in mock if x[k] == v]

        return mock[0]


PyramidJsonRPC.add_route(PyramidJsonRPC.View, '/web/client/view')
