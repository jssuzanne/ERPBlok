from anyblok import Declarations


register = Declarations.register
PyramidJsonRPC = Declarations.PyramidJsonRPC


@register(PyramidJsonRPC)
class View:

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

        return entries.to_dict(*fields)

    @PyramidJsonRPC.rpc_method(request_method='POST')
    def get_entry(self, model=None, primary_keys=None, fields=None, **kwargs):
        Model = self.registry.get(model)
        entry = Model.from_primary_keys(**primary_keys)
        if entry is None or not fields:
            return {}

        return entry.to_dict(*fields)

    @PyramidJsonRPC.rpc_method(request_method='POST')
    def new_entry(self, model=None, fields=None, **kwargs):
        if not fields:
            return {}

        # do a new object without save it in the session, we want get the
        # default value
        entry = self.registry.get(model)()
        return entry.to_dict(*fields)

    def format_values(self, Model, values):
        fields = Model.fields_description()
        vals, x2M = {}, {}
        for k, v in values.items():
            model = fields[k]['model']
            if fields[k]['type'] in ('One2Many', 'Many2Many'):
                x2M[k] = self.registry.get(model).from_multi_primary_keys(*v)
            elif fields[k]['model']:
                vals[k] = self.registry.get(model).from_primary_keys(**v)
            else:
                vals[k] = v

        return vals, x2M

    @PyramidJsonRPC.rpc_method(request_method='POST')
    def set_entry(self, model=None, primary_keys=None, values=None,
                  fields=None, **kwargs):
        Model = self.registry.get(model)
        model = None
        if primary_keys:
            model = Model.from_primary_keys(**primary_keys)
        else:
            model = Model()

        if values:
            vals, x2M = self.format_values(Model, values)
            if vals:
                if primary_keys:
                    model.update(**vals)
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

                if not primary_keys:
                    self.registry.session.add(model)

        if not fields:
            return {}

        for field in Model.get_primary_keys():
            if field not in fields:
                fields.append(field)

        return model.to_dict(*fields)

    @PyramidJsonRPC.rpc_method(request_method='POST')
    def dummy_set_entry(self, model=None, values=None, fields=None, **kwargs):
        Model = self.registry.get(model)
        model = None
        if values:
            vals, x2M = self.format_values(Model, values)
            if vals:
                model = Model.insert(**vals)

            # TODO
            #if x2M:
            #    if not model:
            #        model = Model()

            #    for fname, vals in x2M.items():
            #        with self.registry.session.no_autoflush:
            #            f = getattr(model, fname)
            #            for fv in f:
            #                if fv not in vals:
            #                    f.remove(fv)
            #            for val in vals:
            #                if val not in f:
            #                    f.append(val)

        if not fields:
            return {}

        return model.to_dict(*fields)

    @PyramidJsonRPC.rpc_method(request_method='POST')
    def del_entries(self, model=None, primary_keys=None, **kwargs):
        if not primary_keys:
            return False

        Model = self.registry.get(model)
        for pks in primary_keys:
            Model.from_primary_keys(**pks).delete()

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
        return res


PyramidJsonRPC.add_route(PyramidJsonRPC.View, '/web/client/view')
