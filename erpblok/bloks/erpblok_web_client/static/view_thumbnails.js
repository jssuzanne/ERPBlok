ERPBlok.View.Thumbnails = ERPBlok.View.MultiEntries.extend({
    title_selector: 'Thumbnails view',
    icon_selector: 'fi-thumbnails',
    class_name: 'view-thumbnails',
    template: 'ERPBlokViewThumbnails',
    appendToView: function(line) {
        line.$el.appendTo(this.$el.find('div#thumbnails-' + this.options.id));
    },
    get_entry: function (record) {
        return new ERPBlok.View.Thumbnails.Sticker(this, record);
    },
});
ERPBlok.View.Thumbnails.Sticker = ERPBlok.View.Entry.extend({
    template: 'ERPBlokViewThumbnailsSticker',
    render: function () {
        var self = this;
        this._super();
        this.$el.find('div.selectable:not(button)').click(function () {
            if (self.view.readonly) {
                self.view.transition('selectRecord', {id: self.id});
            }
        });
    },
    get_fields: function () {
        var self = this,
            fields = {};
        $.each(this.view.options.fields2display, function (i, field) {
            var f  = self.view.get_field_cls(field);
            f.set_value(self.record[field.id]);
            fields[field.id] = f;
        });
        return fields;
    },
});
