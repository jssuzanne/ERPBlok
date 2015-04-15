ERPBlok.View.Field = ERPBlok.Model.extend({
    template: 'ERPBlokViewField',
    type: 'text',
    init : function(view, options) {
        this.view = view;
        this.options = options;
    },
    render: function(value) {
        this.set_value(value);
        this.$el = this._render();
    },
    _render: function () {
        var readonly = this.options.readonly || this.view.readonly || false;
        var values = $.extend({}, {
            readonly: readonly,
            type: this.type},
            this.options,
            {value: this.get_render_value()})
        var $el =  $(tmpl(this.template, values));
        $el.find('input').val(this.get_render_value());
        return $el
    },
    set_value: function(value) {
        this.value = value;
    },
    get_render_value: function() {
        return this.value;
    },
    refresh_render: function () {
        var $el = this._render();
        // update the html
        this.$el.replaceWith($el);
        // update the dom
        this.$el = $el;
    },
    get_value: function() {
        var $input = this.$el.find('input')
        if ($input) {
            var val = $input.val();
            if (val == "") return null;
            return val;
        } else {
            return this.get_render_value();
        }
    },
    value_changed: function () {
        if (this.get_value() == this.get_render_value()) {
            return false;
        }
        return true;
    },
});
ERPBlok.View.Field.String = ERPBlok.View.Field.extend({});
ERPBlok.View.Field.Integer = ERPBlok.View.Field.extend({
    type: 'number',
    get_value: function() {
        return Number(this._super());
    },
});
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
