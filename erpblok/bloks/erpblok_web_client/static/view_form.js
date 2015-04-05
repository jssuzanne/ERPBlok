ERPBlok.View.Form = ERPBlok.View.extend({
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
        var fields = this.options.fields;
        for (var i in fields) {
            this.$el.find('#' + fields[i]).text(record[fields[i]]);
        }
    }
});
