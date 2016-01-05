from anyblok import Declarations


register = Declarations.register
PyramidJsonRPC = Declarations.PyramidJsonRPC


@register(PyramidJsonRPC)
class Field:

    @PyramidJsonRPC.rpc_method()
    def many2x_render(self, model=None, primary_keys=None, **kwargs):
        """ return the action render

        :param action: id of the action """
        Model = self.registry.get(model)
        entry = Model.from_primary_keys(**primary_keys)
        return entry.field_render()


PyramidJsonRPC.add_route(PyramidJsonRPC.Field, '/web/client/field')
