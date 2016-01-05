(function () {
    AnyBlokJS.register({
        classname: 'View.MultiEntries',
        extend: ['View'],
        prototype: {
            template: undefined,
            init: function(viewManager, options) {
                this._super(viewManager, options);
                this.entries = [];
            },
            getViewEl: function() {
                var self = this,
                    values = {id: this.options.id,
                              options: this.options,
                              class_name: this.class_name};
                var $el = $(tmpl(this.template, values));
                this.$el = $el;
                return $el;
            },
            render: function (args) {
                this._super(args);
                this.do_search();
            },
            do_search: function () {
                var self = this,
                    fields = $.merge($.merge([], this.options.primary_keys),
                                     this.options.fields),
                    values = this.viewManager.action.actionManager.get_entries_values({
                        model: this.viewManager.action.value.model,
                        fields: fields,
                    });
                this.rpc('get_entries', values, function (records) {
                    self.clear_all();
                    self.render_records(records);
                });
            },
            clear_all: function() {
                if (this.entries.length) {
                    for (var i in this.entries) {
                        if(this.entries[i].$el) {
                            this.entries[i].$el.remove();
                        }
                    }
                    this.entries = [];
                }
            },
            render_records: function(records) {
                for (var i in records) {
                    this.render_record(records[i]);
                }
            },
            appendToView: function(line) {
            },
            get_entry: function (record) {
                return AnyBlokJS.new('View.Entry', this, record);
            },
            render_record: function(record) {
                var line = this.get_entry(record);
                line.render();
                this.appendToView(line);
                this.entries.push(line);
            },
            on_new_entry: function () {
                this.transition('newRecord', {});
            },
            on_delete_entry: function () {
                var self = this,
                    entries_primary_keys = [];
                $.each(this.entries, function(i, line) {
                    if (line.selected) {
                        entries_primary_keys.push(line.id);
                    }
                });
                self.rpc('del_entry', {model: this.viewManager.action.value.model,
                                       primary_keys: entries_primary_keys}, function () {
                    self.do_search();
                });
            },
            on_rpc_call_classmethod: function(dataset) {
                var self = this,
                    entries_primary_keys = [];
                $.each(this.entries, function(i, line) {
                    if (line.selected) {
                        entries_primary_keys.push(line.id);
                    }
                });
                self.rpc('call_classmethod', {model: this.viewManager.action.value.model,
                                              primary_keys: entries_primary_keys,
                                              method: dataset.method,
                                              params: [], kwparams: {}}, function (result) {
                    self.parse_call_result(result);
                });
            },
        },
    });
    AnyBlokJS.register({
        classname: 'View.Entry',
        extend: ['View'],
        prototype: {
            template: undefined,
            init: function(view, record) {
                this.view = view;
                this.record = record;
                this.id = {}
                var primary_keys = view.options.primary_keys;
                for (var i in primary_keys) {
                    this.id[primary_keys[i]] = record[primary_keys[i]];
                }
            },
            render: function() {
                var self = this;
                this.fields = this.get_fields();
                this.$el = $(tmpl(this.template, this.get_values_for_template()));
                // two way (first)
                var two_way_link = {};
                $.each(this.fields, function(id, field) {
                    var key = 'div#' + id + '.field';
                    var $field = self.$el.find(key);
                    two_way_link[id] = {parents: $field, field: field}
                });
                // two way (2nd)
                $.each(two_way_link, function(id, field) {
                    field.field.render(field.parents);
                });
                this.$el.find('button').click(function(event) {
                    event.stopPropagation();
                    var func = event.currentTarget.dataset.function;
                    var method = event.currentTarget.dataset.method || undefined;
                    self.view[func](self.id, method);
                });
            },
            get_fields: function () {
                var self = this,
                    fields = {};
                $.each(this.view.options.fields2display, function (i, field) {
                    var f  = self.view.get_field_cls(field);
                    f.set_value(self.record[field.id]);
                    fields[field.id] = f;
                });
                return fields;
            },
            get_values_for_template: function() {
                return {fields: this.fields, options: this.view.options}
            },
        },
    });
}) ();
