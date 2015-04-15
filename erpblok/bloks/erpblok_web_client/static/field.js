ERPBlok.View.Field = ERPBlok.Model.extend({
    template: 'ERPBlokViewListField',
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
        var values = $.extend({}, this.options, {readonly: readonly},
                              {value: this.get_render_value()})
        return $(tmpl(this.template, values));
    },
    set_value: function(value) {
        this.value = value;
    },
    get_render_value: function() {
        return this.value;
    },
    refresh_render: function () {
        this.$el.replaceWith(this._render());
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
    template: 'ERPBlokViewListOne2Many',
    get_render_value: function() {
        if (this.value.length) return this.value[1];
        return this.value;
    },
});
ERPBlok.View.Field.Many2Many = ERPBlok.View.Field.One2Many.extend({});
