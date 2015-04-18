ERPBlok.View.MultiEntries = ERPBlok.View.extend({
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
        var self = this;
        this.rpc('get_entries', {'model': this.viewManager.action.value.model,
                                 'primary_keys': this.options.primary_keys,
                                 'fields': this.options.fields}, function (records) {
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
        return new ERPBlok.View.Entry(this, record);
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
});
ERPBlok.View.Entry = ERPBlok.Model.extend({
    template: undefined,
    init: function(view, record) {
        this.view = view;
        this.record = record;
        this.id = {}
        this.fields = []
        var primary_keys = view.options.primary_keys;
        for (var i in primary_keys) {
            this.id[primary_keys[i]] = record[primary_keys[i]];
        }
    },
    render: function () {
        var self = this;
        this.$el = $(tmpl(this.template, {
            'fields': this.view.options.fields2display,
            'record': this.record,
            'options': this.view.options,
        }));
        for (var i in this.view.options.fields2display) {
            this.render_field(this.view.options.fields2display[i]);
        }
    },
    appendToEntry: function(field, obj) {
    },
    render_field: function(obj) {
        var field = this.view.get_field_cls(obj);
        this.fields.push(field);
        field.render(this.record[obj.id], true);
        this.appendToEntry(field, obj);
    },
});
