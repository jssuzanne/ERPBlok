ERPBlok.View.Field = ERPBlok.Model.extend({
    template: 'ERPBlokViewField',
    type: 'text',
    init : function(view, options) {
        this.view = view;
        this.options = options;
        this.changed = false;
    },
    render: function() {
        var readonly = this.is_readonly();
        var value = this.get_render_value();
        var values = $.extend({}, {
            readonly: readonly,
            type: this.type},
            this.options,
            {value: value})
        this.$el = $(tmpl(this.template, values));
        if (! readonly) this._render_init_input(value);
    },
    is_readonly: function () {
        return this.options.readonly || this.view.readonly || false;
    },
    _render_init_input: function(value) {
        var self = this;
        this.$el.val(value);
        this.$el.change(function () {
            self.changed = true;
        })
    },
    set_value: function(value) {
        this.value = value;
    },
    get_render_value: function() {
        return this.value;
    },
    get_value: function() {
        if (this.is_readonly()) {
            return this.get_render_value();
        } else {
            var val = this.$el.val();
            if (val == "") return null;
            return val;
        }
    },
});
ERPBlok.View.Field.X2Many= ERPBlok.View.Field.extend({
    template: 'ERPBlokViewX2Many',
});
ERPBlok.View.Field.Action = ERPBlok.View.Field.X2Many.extend(ERPBlok.ActionInterface.prototype, {
    render: function() {
        this._super();
        var action = new ERPBlok.Action(this);
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
});
ERPBlok.View.Field.String = ERPBlok.View.Field.extend({});
ERPBlok.View.Field.Password = ERPBlok.View.Field.String.extend({
    template: 'ERPBlokViewFieldPassword',
});
ERPBlok.View.Field.Integer = ERPBlok.View.Field.extend({
    type: 'number',
    get_value: function() {
        return Number(this._super());
    },
});
ERPBlok.View.Field.Binary = ERPBlok.View.Field.extend({
    template: 'ERPBlokViewFieldBinary',
})
ERPBlok.View.Field.Many2One = ERPBlok.View.Field.extend({});
ERPBlok.View.Field.One2One = ERPBlok.View.Field.Many2One.extend({});
ERPBlok.View.Field.One2Many = ERPBlok.View.Field.Action.extend({});
ERPBlok.View.Field.Many2Many = ERPBlok.View.Field.Action.extend({});
ERPBlok.View.Field.Many2ManyChoices = ERPBlok.View.Field.X2Many.extend({
    template: 'ERPBlokViewMany2ManyChoices',
    render: function() {
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
                var entry = new ERPBlok.View.Many2ManyChoice(
                    self, readonly, record[0], record[1]);
                self.entries.push(entry);
                entry.$el.appendTo(self.$el);
            });
        });
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
});
ERPBlok.View.Many2ManyChoice = ERPBlok.Model.extend({
    init: function(field, readonly, pks, label) {
        var self = this;
        this.pks = pks;
        this.label = label;
        this.field = field;
        this.checked = false;
        this.$el = $(tmpl('ERPBlokViewMany2ManyChoice', {
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
});
