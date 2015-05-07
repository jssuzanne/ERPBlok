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
        this.record = record;
        var self = this,
            fields = this.get_fields(),
            values = {
                fields: fields,
                options: this.options,
            };
        this.$el.children().remove();
        var $el = $(tmpl(this.options.template, values));
        $el.appendTo(this.$el);

        // two way (first)
        var two_way_link = {};
        $.each(fields, function(id, field) {
            var key = 'div#' + id + '.field';
            var $field = $el.find(key);
            two_way_link[id] = {parents: $field, field: field}
        });
        // two way (2nd)
        $.each(two_way_link, function(id, field) {
            field.field.render();
            field.field.$el.appendTo(field.parents);
        });
        $el.find('button').click(function(event) {
            var func = event.currentTarget.dataset.function;
            var method = event.currentTarget.dataset.method || undefined;
            self[func](self.args.id, method);
        });
    },
    get_fields: function() {
        var self = this,
            fields = {};
        $.each(this.options.fields2display, function(i, field) {
            var f = self.get_field_cls(field);
            f.set_value(self.record[field.id]);
            fields[field.id] = f;
            self.fields.push(f);
        });
        return fields;
    },
    refresh_render: function () {
        this.render_record(this.record);
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
                self.render_record(record);
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
