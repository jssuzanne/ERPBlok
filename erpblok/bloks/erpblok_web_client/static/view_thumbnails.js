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
    appendToEntry: function(field, obj) {
        field.$el.appendTo(this.$el.find('#' + obj.id))
    },
    render: function () {
        var self = this;
        this._super();
        this.$el.find('div.selectable').click(function () {
            if (self.view.readonly) {
                self.view.transition('selectRecord', {id: self.id});
            }
        });
    },
});
