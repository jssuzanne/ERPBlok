ERPBlok.View.List = ERPBlok.View.extend(ERPBlok.RPC.prototype, {
    'rpc_url': '/web/client/view',
    icon_url_selector: '/static/menus/toggle-small-expand.gif',  // TODO replace by other
    title_selector: 'List view',
    class_name: 'view-list',
    lines: [],
    render: function () {
        this.do_search();
    },
    do_search: function () {
        var self = this;
        this.rpc('get_entries', {'model': this.viewManager.model,
                                 'primary_keys': this.pks,
                                 'fields': this.fields}, function (records) {
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
        this.lines.push(line.$el);
    }
});
ERPBlok.View.List.Line = ERPBlok.Model.extend({
    init: function(view, record) {
        this.view = view;
        this.record = record;
    },
    render: function () {
        var id = "plop";
        var el = '<tr>';
        for (var i in this.view.fields) {
            // TODO replace by field
            el += '<td id="' + this.view.fields[i] + '">';
            el += this.record[this.view.fields[i]];
            el += '</td>';
        }
        el += '</tr>';
        this.$el = $(el);
    },
});
