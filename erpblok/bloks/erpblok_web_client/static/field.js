(function() {
    AnyBlokJS.register({
        classname: 'Field.X2Many',
        extend: ['ActionInterface', 'Field'],
        prototype: {
            init: function(view, options) {
                this._super(view, options);
            },
            template: 'ERPBlokViewX2Many',
        },
    });
    AnyBlokJS.register({
        classname: 'Field.Action',
        extend: ['Field.X2Many'],
        prototype: {
            render: function($parentel) {
                this._super($parentel);
                var action = AnyBlokJS.new('Action', this);
                action.load(this.options.action);
                action.$el.appendTo(this.$el);
            },
            get_entries_values: function (values) {
                var pks = [];
                if (this.value.length) {
                    $.each(this.value[1], function(i, val) {
                        pks.push(val[0])
                    });
                }
                return $.extend({}, values,
                                {primary_keys: pks, comefromfield: true});
            },
        },
    });
    AnyBlokJS.register({
        classname: 'Field.String',
        extend: ['Field'],
        prototype: {},
    });
    AnyBlokJS.register({
        classname: 'Field.Password',
        extend: ['Field.String'],
        prototype: {
            template: 'ERPBlokViewFieldPassword',
        },
    });
    AnyBlokJS.register({
        classname: 'Field.Integer',
        extend: ['Field'],
        prototype: {
            type: 'number',
            get_value: function() {
                return Number(this._super());
            },
        },
    });
    AnyBlokJS.register({
        classname: 'Field.Binary',
        extend: ['Field'],
        prototype: {
            template: 'ERPBlokViewFieldBinary',
            render_template: function($parentel) {
                this._super($parentel);
                this.$el.attr('src', this.get_render_value())
            },
        },
    });
    AnyBlokJS.register({
        classname: 'Field.Many2One',
        extend: ['RPC', 'Field'],
        prototype: {
            template: 'ERPBlokViewFieldx2One',
            get_render_value: function() {
                return this.render_value || '';
            },
            render: function($parentel) {
                var self = this;
                var _super = this._super;
                this.rpc('many2x_render', {model: this.options.model, primary_keys: this.value},
                         function(render_value) {
                    self.render_value = render_value;
                    _super.apply(self, $parentel);
                    self.$el.find('a').click(function() {
                        var action = AnyBlokJS.new('Action');
                        action.load(self.options.action,
                                    self.options.action.selected,
                                    JSON.stringify(self.value[0]));
                    });
                });
            },
        },
    });
    AnyBlokJS.register({
        classname: 'Field.One2One',
        extend: ['Field.Many2One'],
        prototype: {},
    });
    AnyBlokJS.register({
        classname: 'Field.One2Many',
        extend: ['Field.Action'],
        prototype: {},
    });
    AnyBlokJS.register({
        classname: 'Field.Many2Many',
        extend: ['Field.Action'],
        prototype: {},
    });
    AnyBlokJS.register({
        classname: 'Field.Many2ManyChoices',
        extend: ['Field.X2Many'],
        prototype: {
            template: 'ERPBlokViewMany2ManyChoices',
            render: function($parentel) {
                var self = this,
                    readonly = this.is_readonly(),
                    value = this.get_render_value(),
                    values = {
                        model: this.options.model,
                        display: this.options.display || null,
                    };
                $.each(['smallgrid', 'mediumgrid', 'largegrid'], function(i, k){
                    if (!self.options[k]) {
                        self.options[k] = 1;
                    }
                })
                this._super();
                this.entries = [];
                this.changed = false;
                this.view.rpc('get_relationship_entries', values, function (records) {
                    $.each(records, function(i, record) {
                        var entry = AnyBlokJS.new('View.Many2ManyChoice', self, readonly, record[0], record[1]);
                        self.entries.push(entry);
                        entry.$el.appendTo(self.$el);
                    });
                });
                this.$el.appendTo($parentel);
            },
            get_render_value: function() {
                var vals = [];
                $.each(this.value, function(i, val) {
                    vals.push(val[0]);
                });
                return vals;
            },
            get_value: function() {
                if (this.is_readonly() || !this.changed) {
                    return this.get_render_value();
                } else {
                    var vals = [];
                    $.each(this.entries, function(i, entry) {
                        if (entry.checked) {
                            vals.push(entry.pks);
                        }
                    });
                    return vals
                }
            },
        },
    });
    AnyBlokJS.register({
        classname: 'View.Many2ManyChoice',
        prototype: {
            init: function(field, readonly, pks, label) {
                var self = this;
                this.pks = pks;
                this.label = label;
                this.field = field;
                this.checked = false;
                this.$el = $($.templates('#ERPBlokViewMany2ManyChoice').render({
                    options: field.options,
                    label: label,
                    readonly: readonly,
                }));
                $.each(field.get_render_value(), function(i, value) {
                    if (_.isEqual(value, pks)) {
                        self.$el.find('input').prop('checked', true);
                        self.checked = true;
                    }
                });
                this.$el.find('input').change(function() {
                    self.checked = self.$el.find('input').prop('checked');
                    field.view.changed = true;
                });
            },
        },
    });
}) ();
