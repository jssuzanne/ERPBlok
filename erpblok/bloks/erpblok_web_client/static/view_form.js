(function() {
    AnyBlokJS.register({
        classname: 'View.Form',
        extend: ['View'],
        prototype: {
            title_selector: 'Form view',
            class_name: 'view-form',
            icon_selector: 'fi-page',
            init: function(viewManager, options) {
                this._super(viewManager, options);
                this.fields = {};
                this.fields_by_ids = {};
                this.changed_record = {};
            },
            getViewEl: function ($action) {
                this._super($action);
                var $el = $($.templates(this.options.template).render());
                $el.appendTo(this.$el);
                this.apply_react_components();
                return this.$el;
            },
            render: function (args) {
                this._super(args);
                var self = this;
                this.args = args;
                if(args && args.id) {
                    this.rpc('get_entry', {'model': this.viewManager.action.value.model,
                                           'primary_keys': args.id,
                                           'fields': this.options.fields}, function (record) {
                        self.applyRecord(record);
                    });
                } else if (args && args.new){
                    this.toggleReadonly();
                    this.rpc('new_entry', {model: this.viewManager.action.value.model,
                                           fields: this.options.fields}, function (record) {
                        self.applyRecord(record);
                    });
                }
            },
            apply_react_components: function() {
                this.apply_fields();
            },
            apply_fields: function() {
                var self = this;
                $.each(this.options.fields2display, function (i, field) {
                    var options = $.extend(
                        {}, field, {value: undefined,
                                    actionManager: self.viewManager.action.actionManager});
                    var $els = self.$el.find('field#' + field.id);
                    for (i=0; i<$els.length; i++) {
                        self.apply_field(options, $els[i]);
                    }
                });
            },
            get_field: function(field_id){
                for (var i in this.options.fields2display) {
                    if (this.options.fields2display[i].id == field_id) {
                        return this.options.fields2display[i];
                    }
                }
            },
            initField: function (field_id, instance) {
                var field_name = this.get_field(field_id).field_name;
                if (this.fields[field_name] == undefined) {
                    this.fields[field_name] = [];
                }
                this.fields[field_name].push(instance);
                this.fields_by_ids[field_id] = instance;
            },
            isReadonly: function (field_id) {
                var field = this.get_field(field_id);
                return this.readonly || field.readonly || false;
            },
            updateField: function (field_id, value) {
                var field_name = this.get_field(field_id).field_name;
                for (var i in this.fields[field_name]) {
                    this.fields[field_name][i].setState({value: value});
                }
                var isArray = false;
                if (Array.isArray(value) || Array.isArray(this.record[field_name]))
                    isArray = true;

                if (isArray || (value != this.record[field_name])) {
                    this.changed_record[field_name] = value;
                } else {
                    if (this.changed_record[field_name]) {
                        delete this.changed_record[field_name];
                    }
                }
            },
            pressEnter: function () {
            },
            get_value_of: function (field_name) {
                return this.changed_record[field_name] || this.record[field_name];
            },
            apply_field: function (options, $el) {
                ReactDOM.render(<Field options={options}
                                       init_field={this.initField.bind(this)}
                                       is_readonly={this.isReadonly.bind(this)}
                                       pressEnter={this.pressEnter.bind(this)}
                                       get_value_of={this.get_value_of.bind(this)}
                                       update_field={this.updateField.bind(this)} />,
                                $el);
            },
            applyReadOnly: function () {
                this._super();
                if (this.record) this.applyRecord();
            },
            applyRecord: function (record) {
                var self = this;
                if (record) this.record = record;
                $.each(this.options.fields2display, function (i, field) {
                    self.fields_by_ids[field.id].setState({
                        value: self.record[field.field_name],
                        readonly: self.isReadonly(field.id)});
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
            on_save_view: function () {
                var self = this;
                var values = this.changed_record;
                this.toggleReadonly();
                this.rpc('set_entry', {model: this.viewManager.action.value.model,
                                       primary_keys: this.args.id,
                                       values: values,
                                       fields: this.options.fields}, function (record) {
                    self.applyRecord(record);
                    if (!self.args.id){
                        self.args.id = {};
                        $.each(self.options.primary_keys, function(i, pk) {
                            self.args.id[pk] = record[pk];
                        });
                    }
                });
            },
            on_new_entry: function () {
                var self = this;
                this.toggleReadonly();
                this.args.id = null;
                this.rpc('new_entry', {model: this.viewManager.action.value.model,
                                       fields: this.options.fields}, function (record) {
                    self.applyRecord(record);
                });
            },
            on_delete_entry: function() {
                var self = this;
                this.rpc('del_entry', {model: this.viewManager.action.value.model,
                                       primary_keys: [this.args.id]}, function () {
                    self.transition('closeView');
                });
            },
            on_read_view: function() {
                if (! this.readonly) {
                    this.toggleReadonly();
                }
                this.changed_record = {};
                if (! this.args.id || Object.getOwnPropertyNames(this.args.id).length == 0) {
                    this.transition('closeView');
                }
            },
        },
    });
}) ();
