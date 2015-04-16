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
        } else if (args && args.new){
            this.toggleReadonly();
            this.rpc('set_entry', {model: this.viewManager.action.value.model,
                                   primary_keys: null,
                                   values: null,
                                   fields: this.options.fields}, function (record) {
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
            field.render(record[item.id], true);
            field.$el.appendTo(node);
        });
    },
    refresh_render: function () {
        $.each(this.fields, function (i, field) {
            field.render();
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
                    field.render(record[field.options.id])
                });
                if (!self.args.id){
                    self.args.id = {};
                    $.each(self.options.primary_keys, function(i, pk) {
                        self.args.id[pk] = record[pk];
                    });
                }
            }
        });
    },
    on_new_entry: function () {
        var self = this;
        this.toggleReadonly();
        this.args.id = null;
        this.rpc('set_entry', {model: this.viewManager.action.value.model,
                               primary_keys: null,
                               values: null,
                               fields: this.options.fields}, function (record) {
            if (record) {
                $.each(self.fields, function (i, field) {
                    field.render(record[field.options.id], true)
                });
            }
        });
    },
    on_delete_entry: function() {
        var self = this;
        this.rpc('del_entry', {model: this.viewManager.action.value.model,
                               primary_keys: [this.args.id]}, function () {
            self.transition('closeView');
        });
    },
    get_values_changed: function () {
        var res = {},
            self = this;
        $.each(this.fields, function(i, field) {
            if (field.changed) {
                res[field.options.id] = field.get_value()
            }
        });
        return res;
    },
});
