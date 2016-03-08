from anyblok import Declarations


register = Declarations.register
PyramidJsonRPC = Declarations.PyramidJsonRPC


@register(PyramidJsonRPC)
class Field:

    @PyramidJsonRPC.rpc_method()
    def x2One_render(self, model=None, primary_keys=None, **kwargs):
        """ return the action render

        :param action: id of the action """
        Model = self.registry.get(model)
        entry = Model.from_primary_keys(**primary_keys)
        return entry.field_render()

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
