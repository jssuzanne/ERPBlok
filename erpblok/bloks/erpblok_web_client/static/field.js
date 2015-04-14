ERPBlok.View.Field = ERPBlok.Model.extend({
    template: 'ERPBlokViewListField',
    render: function(obj, value) {
        this.set_value(value);
        this.$el = $(tmpl(this.template, 
                          $.extend({}, obj, {value: this.get_render_value()})))
    },
    set_value: function(value) {
        this.value = value;
    },
    get_render_value: function() {
        return this.value;
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
