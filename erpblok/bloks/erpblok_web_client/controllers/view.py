from anyblok import Declarations


register = Declarations.register
PyramidJsonRPC = Declarations.PyramidJsonRPC


@register(PyramidJsonRPC)
class View:

    def get_field_value(self, entry, field):
        value = getattr(entry, field)
        if not value:
            return value

        model = entry.__registry_name__

        def get_query(Model):
            query = Model.query()
            query = query.filter(Model.model == model)
            return query.filter(Model.name == field)

        if get_query(self.registry.System.Column).count():
            return value

        if get_query(self.registry.System.Field).count():
            return value

        RelationShip = self.registry.System.RelationShip
        query = get_query(RelationShip)
        if query.count():
            rs = query.first()
            if rs.ftype in ('Many2One', 'One2One'):
                return model, value.field_render()
            else:
                return model, [x.field_render() for x in value]

    @PyramidJsonRPC.rpc_method(request_method='POST')
    def get_entries(self, model=None, primary_keys=None, fields=None, **kwargs):
        Model = self.registry.get(model)
        query = Model.query()
        return [{x: self.get_field_value(y, x) for x in primary_keys + fields}
                for y in query.all()]

    @PyramidJsonRPC.rpc_method(request_method='POST')
    def get_entry(self, model=None, primary_keys=None, fields=None, **kwargs):
        Model = self.registry.get(model)
        model = Model.from_primary_keys(**primary_keys)
        return {x: self.get_field_value(model, x) for x in fields}

    @PyramidJsonRPC.rpc_method(request_method='POST')
    def set_entry(self, model=None, primary_keys=None, values=None,
                  fields=None, **kwargs):

        values = {x: y for x, y in values.items() if x not in primary_keys}
        Model = self.registry.get(model)
        model = Model.from_primary_keys(**primary_keys)
        if values:
            model.update(values)
            self.registry.commit()

        return {x: self.get_field_value(model, x) for x in fields}


PyramidJsonRPC.add_route(PyramidJsonRPC.View, '/web/client/view')
