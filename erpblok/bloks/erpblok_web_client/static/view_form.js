ERPBlok.View.Form = ERPBlok.View.extend({
    title_selector: 'Form view',
    class_name: 'view-form',
    icon_selector: 'fi-page',
    init: function(viewManager, options) {
        this._super(viewManager, options);
        this.fields = []
    },
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
        var self = this;
        $.each(this.options.fields2display, function(i, item) {
            var node = self.$el.find('#' + item.id),
                field = self.get_field_cls(item.type);
            node.children().remove();
            self.fields.push(field);
            field.render(item, record[item.id]);
            field.$el.appendTo(node);
        });
    }
});
