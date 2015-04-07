ERPBlok.View.Form = ERPBlok.View.extend({
    title_selector: 'Form view',
    class_name: 'view-form',
    lines: [],
    render: function (args) {
        var self = this;
        if(args && args.id) {
            this.rpc('get_entry', {'model': this.viewManager.action.value.model,
                                   'primary_keys': args.id,
                                   'fields': this.options.fields}, function (record) {
                if (record) {
                    self.render_record(record);
                }
            });
        }
    },
    render_record: function(record) {
        var fields = this.options.fields;
        for (var i in fields) {
            this.$el.find('#' + fields[i]).text(record[fields[i]]);
        }
    }
});
