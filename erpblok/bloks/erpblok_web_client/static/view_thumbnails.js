(function () {
    AnyBlokJS.register({
        classname: 'View.Thumbnails',
        extend: ['View.MultiEntries'],
        prototype: {
            title_selector: 'Thumbnails view',
            icon_selector: 'fi-thumbnails',
            class_name: 'view-thumbnails',
            template: 'ERPBlokViewThumbnails',
            appendToView: function(line) {
                line.$el.appendTo(this.$el.find('div#thumbnails-' + this.options.id));
            },
            get_entry: function (record) {
                return AnyBlokJS.new('View.Thumbnails.Sticker', this, record);
            },
        },
    });
    AnyBlokJS.register({
        classname: 'View.Thumbnails.Sticker',
        extend: ['View.Entry'],
        prototype: {
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
            render_template: function () {
                this.$el = $($.templates('#' + this.template).render());
                var $el = $($.templates(this.view.options.template).render(
                   this.get_values_for_template()));
                $el.appendTo(this.$el.find('.view-contnair'))
            },
        },
    });
}) ();
