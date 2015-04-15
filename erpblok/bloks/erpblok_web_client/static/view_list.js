ERPBlok.View.List = ERPBlok.View.extend({
    title_selector: 'List view',
    icon_selector: 'fi-list',
    class_name: 'view-list',
    init: function(viewManager, options) {
        this._super(viewManager, options);
        this.lines = [];
    },
    getViewEl: function() {
        var $el = $(tmpl('ERPBlokViewList', {
            id: this.options.id,
            class_name: this.class_name,
            headers: this.options.headers,
        }));
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
        if (this.lines.length) {
            for (var i in this.lines) {
                if(this.lines[i].$el) {
                    this.lines[i].$el.remove();
                }
            }
            this.lines = [];
        }
    },
    render_records: function(records) {
        for (var i in records) {
            this.render_record(records[i]);
        }
    },
    render_record: function(record) {
        var line = new ERPBlok.View.List.Line(this, record);
        line.render();
        line.$el.appendTo(this.$el.find('tbody'));
        this.lines.push(line);
    }
});
ERPBlok.View.List.Line = ERPBlok.Model.extend({
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
        this.$el = $(tmpl('ERPBlokViewListLine', {
            'fields': this.view.options.fields2display,
            'record': this.record,
        }));
        for (var i in this.view.options.fields2display) {
            this.render_field(this.view.options.fields2display[i]);
        }
        this.$el.click(function () {
            self.view.transition('selectRecord', {id: self.id});
        });
    },
    render_field: function(obj) {
        var field = this.view.get_field_cls(obj);
        this.fields.push(field);
        field.render(this.record[obj.id]);
        field.$el.appendTo(this.$el.find('td#' + obj.id))
    },
});
