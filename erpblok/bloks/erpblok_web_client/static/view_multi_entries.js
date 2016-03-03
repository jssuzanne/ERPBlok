(function () {
    AnyBlokJS.register({
        classname: 'View.MultiEntries',
        extend: ['Template', 'View'],
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
                this.$el = this.render_template(values);
                return this.$el;
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
                    self.records = records;
                    for (var i in records) {
                        self.render_record(records[i]);
                    }
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
            appendToView: function(entry) {},
            get_entry: function (index) {
                return AnyBlokJS.new('View.Entry', this, index);
            },
            render_record: function(record) {
                var entry = this.get_entry(record);
                entry.render();
                this.appendToView(entry);
                this.entries.push(entry);
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
        extend: ['Template', 'View'],
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
            initField: function (field_id, instance) {
            },
            isReadonly: function (field_id) {
                return true;
            },
            updateField: function (field_id, value) {
            },
            apply_react_componente: function (options, $el) {
                ReactDOM.render(<Field options={options}
                                       init_field={this.initField.bind(this)}
                                       is_readonly={this.isReadonly.bind(this)}
                                       update_field={this.updateField.bind(this)} />,
                                $el);
            },
            render: function() {
                var self = this;
                this.fields = this.get_fields();
                this.$el = this.render_template(this.get_values_for_template());
                this.view.appendToView(this);
                $.each(this.view.options.fields2display, function (i, field) {
                    var options = $.extend(
                        {}, field, {value: self.record[field.field_name]});
                    var $els = self.$el.find('field#' + field.id);
                    for (i=0; i<$els.length; i++) {
                        self.apply_react_componente(options, $els[i]);
                    }
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
                    fields = [];
                $.each(this.view.options.fields2display, function (i, field) {
                    fields.push({id: field.id})
                });
                return fields;
            },
            get_values_for_template: function() {
                return {fields: this.fields, options: this.view.options}
            },
        },
    });
}) ();
