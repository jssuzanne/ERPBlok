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
        var html = tmpl(this.template, values);
        if (! readonly) this._render_init_input($(html), value);
        return html;
    },
    is_readonly: function () {
        return this.options.readonly || this.view.readonly || false;
    },
    _render_init_input: function($el, value) {
        debugger
        var self = this;
        $el.val(value);
        $el.change(function () {
            debugger
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
ERPBlok.View.Field.String = ERPBlok.View.Field.extend({});
ERPBlok.View.Field.Integer = ERPBlok.View.Field.extend({
    type: 'number',
    get_value: function() {
        return Number(this._super());
    },
});
ERPBlok.View.Field.Binary = ERPBlok.View.Field.extend({
    template: 'ERPBlokViewFieldBinary',
})
ERPBlok.View.Field.Many2One = ERPBlok.View.Field.extend({
    get_render_value: function() {
        if (this.value) return this.value[1][1];
        return this.value;
    },
});
ERPBlok.View.Field.One2One = ERPBlok.View.Field.Many2One.extend({});
ERPBlok.View.Field.One2Many = ERPBlok.View.Field.extend({
    template: 'ERPBlokViewOne2Many',
    get_render_value: function() {
        if (this.value.length) return this.value[1];
        return this.value;
    },
});
ERPBlok.View.Field.Many2Many = ERPBlok.View.Field.One2Many.extend({});
