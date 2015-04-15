ERPBlok.View.Form = ERPBlok.View.extend({
    title_selector: 'Form view',
    class_name: 'view-form',
    icon_selector: 'fi-page',
    init: function(viewManager, options) {
        this._super(viewManager, options);
        this.fields = [];
    },
    render: function (args) {
        this._super(args);
        var self = this;
        this.args = args;
        if(args && args.id) {
            this.rpc('get_entry', {'model': this.viewManager.action.value.model,
                                   'primary_keys': args.id,
                                   'fields': this.options.fields}, function (record) {
                if (record) {
                    self.render_record(record);
                }
            });
        }
    },
    render_record: function(record) {
        var self = this;
        $.each(this.options.fields2display, function(i, item) {
            var node = self.$el.find('#' + item.id),
                field = self.get_field_cls(item);
            node.children().remove();
            self.fields.push(field);
            field.render(record[item.id]);
            field.$el.appendTo(node);
        });
    },
    refresh_render: function () {
        $.each(this.fields, function (i, field) {
            field.refresh_render();
        });
    },
    on_save_view: function () {
        var self = this;
        var values = this.get_values_changed();
        this.toggleReadonly();
        this.rpc('set_entry', {model: this.viewManager.action.value.model,
                               primary_keys: this.args.id,
                               values: values,
                               fields: this.options.fields}, function (record) {
            if (record) {
                $.each(self.fields, function (i, field) {
                    field.set_value(record[field.options.id])
                    field.refresh_render();
                });
            }
        });
    },
    get_values_changed: function () {
        var res = {},
            self = this;
        $.each(this.fields, function(i, field) {
            if (field.value_changed()) {
                res[field.options.id] = field.get_value()
            }
        });
        return res;
    },
});
