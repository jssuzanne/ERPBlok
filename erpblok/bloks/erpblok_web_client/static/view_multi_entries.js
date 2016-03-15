(function () {
    function check_eval (condition, fields) {return eval(condition);}
    AnyBlokJS.register({
        classname: 'View.MultiEntries',
        extend: ['Template', 'View'],
        prototype: {
            template: undefined,
            init: function(viewManager, options) {
                this._super(viewManager, options);
                this.entries = [];
            },
            getViewEl: function($action) {
                var self = this,
                    values = {id: this.options.id,
                              options: this.options,
                              class_name: this.class_name};
                this.$el = this.render_template(values);
                this.$el.appendTo($action);
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
            remove_entry: function (entry) {
                var index = this.entries.indexOf(entry);
                this.entries.splice(index, 1);
                if (entry.$el) entry.$el.remove();
            },
            appendToView: function(entry) {},
            get_entry: function (record, reaonly=true) {
                return AnyBlokJS.new('View.Entry', this, record, readonly);
            },
            render_records: function(records) {
                for (var i in records) {
                    var entry = this.render_record(records[i]);
                    this.appendToView(entry);
                }
            },
            render_record: function(record, readonly=true) {
                var entry = this.get_entry(record, readonly);
                entry.render();
                this.entries.push(entry);
                return entry;
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
                self.rpc('del_entries', {model: this.viewManager.action.value.model,
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
            get_field: function(field_id){
                for (var i in this.options.fields2display) {
                    if (this.options.fields2display[i].id == field_id) {
                        return this.options.fields2display[i];
                    }
                }
            },
        },
    });
    AnyBlokJS.register({
        classname: 'View.Entry',
        extend: ['Template', 'View'],
        prototype: {
            template: undefined,
            init: function(view, record, readonly=true) {
                this.view = view;
                this.record = record;
                this.id = {}
                this.compute_id();
                this.readonly = readonly;
                this.fields = {};
                this.fields_by_ids = {};
                this.changed_record = {};
            },
            compute_id: function () {
                var primary_keys = this.view.options.primary_keys;
                for (var i in primary_keys) {
                    this.id[primary_keys[i]] = this.record[primary_keys[i]];
                }
            },
            initField: function (field_id, instance) {
                var field_name = this.view.get_field(field_id).field_name;
                if (this.fields[field_name] == undefined) {
                    this.fields[field_name] = [];
                }
                this.fields[field_name].push(instance);
                this.fields_by_ids[field_id] = instance;
            },
            isReadonly: function (field_id) {
                var field = this.view.get_field(field_id);
                return this.readonly || field.readonly || false;
            },
            updateField: function (field_id, value) {
                var field_name = this.view.get_field(field_id).field_name;
                for (var i in this.fields[field_name]) {
                    this.fields[field_name][i].setState({value: value});
                }
                var self = this,
                    fields_value = $.extend({}, this.record, this.changed_record);
                $.each(this.view.options.fields2display, function (i, field) {
                    self.fields_by_ids[field.id].setState({all_fields_value: fields_value});
                });
                this.updateVisibilityUI();
            },
            pressEnter: function () {
            },
            get_value_of: function (field_name) {
                return this.changed_record[field_name] || this.record[field_name];
            },
            apply_react_componente: function (options, $el) {
                ReactDOM.render(<Field options={options}
                                       init_field={this.initField.bind(this)}
                                       is_readonly={this.isReadonly.bind(this)}
                                       pressEnter={this.pressEnter.bind(this)}
                                       get_value_of={this.get_value_of.bind(this)}
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
                        {}, field, {value: self.record[field.field_name],
                                    all_fields_value: self.record,
                                    actionManager: self.view.viewManager.action.actionManager});
                    var $els = self.$el.find('field#' + field.id);
                    for (i=0; i<$els.length; i++) {
                        self.apply_react_componente(options, $els[i]);
                    }
                });
                this.updateVisibilityUI();
                this.$el.find('button').click(function(event) {
                    event.stopPropagation();
                    var func = event.currentTarget.dataset.function;
                    var method = event.currentTarget.dataset.method || undefined;
                    self.view[func](self.id, method);
                });
            },
            updateVisibilityUI: function () {
                var fields_value = $.extend({}, this.record, this.changed_record);
                $.each(this.$el.find('.visibility-conditional-ui'), function (i, el) {
                    var condition = el.getAttribute("visible-only-if"); 
                    if (!check_eval(condition, fields_value)) $(el).addClass('hide');
                    else $(el).removeClass('hide');
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
