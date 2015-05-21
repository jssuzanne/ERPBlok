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
                return value.field_render()
            else:
                return [x.field_render() for x in value]

    @PyramidJsonRPC.rpc_method(request_method='POST')
    def get_entries(self, model=None, primary_keys=None, fields=None,
                    comefromfield=False, **kwargs):
        Model = self.registry.get(model)
        entries = None
        if comefromfield:
            if primary_keys:
                entries = Model.from_multi_primary_keys(*primary_keys)
        else:
            entries = Model.query().all()

        if not fields or not entries:
            return []

        return [{x: self.get_field_value(y, x) for x in fields}
                for y in entries]

    @PyramidJsonRPC.rpc_method(request_method='POST')
    def get_relationship_entries(self, model=None, display=None, **kwargs):
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

    @PyramidJsonRPC.rpc_method(request_method='POST')
    def get_entry(self, model=None, primary_keys=None, fields=None, **kwargs):
        Model = self.registry.get(model)
        model = Model.from_primary_keys(**primary_keys)
        return {x: self.get_field_value(model, x) for x in fields}

    def format_values(self, Model, values):
        fields = Model.fields_description()
        vals, x2M = {}, {}
        for k, v in values.items():
            model = fields[k]['model']
            if fields[k]['primary_key']:
                continue
            elif fields[k]['type'] in ('One2Many', 'Many2Many'):
                x2M[k] = self.registry.get(model).from_multi_primary_keys(*v)
            elif fields[k]['model']:
                vals[k] = self.registry.get(model).from_primary_keys(**v)
            else:
                vals[k] = v

        return vals, x2M

    @PyramidJsonRPC.rpc_method(request_method='POST')
    def set_entry(self, model=None, primary_keys=None, values=None,
                  fields=None, autocomit=True, **kwargs):
        Model = self.registry.get(model)
        if primary_keys:
            model = Model.from_primary_keys(**primary_keys)
        else:
            model = Model()

        if values:
            vals, x2M = self.format_values(Model, values)
            if primary_keys:
                if vals:
                    model.update(vals)
            else:
                model = Model.insert(**vals)

            if x2M:
                for fname, vals in x2M.items():
                    with self.registry.session.no_autoflush:
                        f = getattr(model, fname)
                        for fv in f:
                            if fv not in vals:
                                f.remove(fv)
                        for val in vals:
                            if val not in f:
                                f.append(val)

        if autocomit:
            self.registry.commit()

        return {x: self.get_field_value(model, x) for x in fields}

    @PyramidJsonRPC.rpc_method(request_method='POST')
    def del_entry(self, model=None, primary_keys=None, **kwargs):

        if not primary_keys:
            return False

        Model = self.registry.get(model)
        for pks in primary_keys:
            Model.from_primary_keys(**pks).delete()

        self.registry.commit()
        return True

    @PyramidJsonRPC.rpc_method(request_method='POST')
    def call(self, model=None, primary_keys=None, method=None, params=None,
             kwparams=None, **kwargs):
        if not primary_keys:
            return False

        if params is None:
            params = tuple()

        if kwparams is None:
            kwparams = dict()

        Model = self.registry.get(model)
        res = getattr(Model.from_primary_keys(**primary_keys), method)(
            *params, **kwparams)
        self.registry.commit()
        return res

    @PyramidJsonRPC.rpc_method(request_method='POST')
    def call_classmethod(self, model=None, primary_keys=None, method=None,
                         params=None, kwparams=None, **kwargs):
        if params is None:
            params = tuple()

        if kwparams is None:
            kwparams = dict()

        Model = self.registry.get(model)
        res = getattr(Model, method)(
            primary_keys, *params, **kwparams)
        self.registry.commit()
        return res


PyramidJsonRPC.add_route(PyramidJsonRPC.View, '/web/client/view')
