from anyblok import Declarations


register = Declarations.register
PyramidJsonRPC = Declarations.PyramidJsonRPC


@register(PyramidJsonRPC)
class View:

    def get_field_value(self, entry, field):
        value = getattr(entry, field)
        if not value:
            return value

        def get_query(Model):
            query = Model.query()
            query = query.filter(Model.model == entry.__registry_name__)
            return query.filter(Model.name == field)

        Column = self.registry.System.Column
        query = get_query(Column)
        if query.count():
            return value

        Field = self.registry.System.Field
        query = get_query(Field)
        if query.count():
            return value

        RelationShip = self.registry.System.RelationShip
        query = get_query(RelationShip)
        if query.count():
            rs = query.first()
            if rs.rtype in ('Many2One', 'One2One'):
                return value.render()
            else:
                return [x.render() for x in value]

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


PyramidJsonRPC.add_route(PyramidJsonRPC.View, '/web/client/view')
