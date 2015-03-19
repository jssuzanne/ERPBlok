ERPBlok.View.Form = ERPBlok.View.extend(ERPBlok.RPC.prototype, {
    'rpc_url': '/web/client/view',
    icon_url_selector: '/static/menus/toggle-small.gif',  // TODO replace by other
    title_selector: 'Form view',
    class_name: 'view-form',
    lines: [],
    render: function () {
        var self = this;
        this.rpc('get_entries', {'model': this.viewManager.model,
                                 'primary_keys': this.pks,
                                 'fields': this.fields}, function (records) {
            if (records.length) {
                self.render_record(records[0]);
            }
        });
    },
    render_record: function(record) {
        for (var i in this.fields) {
            this.$el.find('#' + this.fields[i]).text(record[this.fields[i]]);
        }
    }
});
