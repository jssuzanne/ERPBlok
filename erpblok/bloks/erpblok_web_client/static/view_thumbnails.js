(function () {
    AnyBlokJS.register({
        classname: 'View.Thumbnails',
        extend: ['View.MultiEntries'],
        prototype: {
            title_selector: 'Thumbnails view',
            icon_selector: 'fi-thumbnails',
            class_name: 'view-thumbnails',
            template: 'ViewThumbnails',
            appendToView: function(line) {
                line.$el.appendTo(this.$el.find('div#thumbnails-' + this.options.id));
            },
            get_entry: function (record, readonly=true) {
                console.log('get entry')
                return AnyBlokJS.new('View.Thumbnails.Sticker', this, record, readonly);
            },
        },
    });
    AnyBlokJS.register({
        classname: 'View.Thumbnails.Sticker',
        extend: ['View.Entry'],
        prototype: {
            template: 'ViewThumbnailsSticker',
            render: function () {
                var self = this;
                this._super();
                this.$el.find('div.selectable:not(button)').click(function () {
                    if (self.view.readonly) {
                        self.view.transition('selectRecord', {id: self.id});
                    }
                });
            },
            render_template: function (values={}) {
                var $el = this._super()
                var $subel = $($.templates(this.view.options.template).render(values));
                $subel.appendTo($el.find('.view-contnair'))
                return $el;
            },
        },
    });
}) ();
