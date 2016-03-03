(function () {
    AnyBlokJS.register({
        classname: 'View.List',
        extend: ['View.MultiEntries'],
        prototype: {
            title_selector: 'List view',
            icon_selector: 'fi-list',
            class_name: 'view-list',
            template: 'ViewList',
            getViewEl: function() {
                var self = this;
                var $el = this._super();
                $el.find('input#all_checkbox').click(function (event) {
                    var checked = $(event.currentTarget).prop('checked');
                    self.$el.find('input#line_checkbox').prop('checked', checked);
                    self.hide_show_buttons()
                });
                return $el;
            },
            appendToView: function(line) {
                line.$el.appendTo(this.$el.find('tbody'));
            },
            get_entry: function (record) {
                return AnyBlokJS.new('View.List.Line', this, record);
            },
            hide_show_buttons: function() {
                var checked = this.$el.find('input#line_checkbox:checked').length;
                this.viewManager.$buttons.find('.on-readonly').addClass('hide');
                this.viewManager.$buttons.find('.on-selected').addClass('hide');
                this.viewManager.$buttons.find('.on-readwrite').addClass('hide');
                if (this.readonly && checked) {
                    this.viewManager.$buttons.find('.on-readonly.on-selected, .on-readonly:not(.on-selected)').removeClass('hide');
                } else if (this.readonly) {
                    this.viewManager.$buttons.find('.on-readonly:not(.on-selected)').removeClass('hide');
                } else {
                    if (checked) {
                        this.viewManager.$buttons.find('.on-selected:not(.on-readonly)').removeClass('hide');
                        this.viewManager.$buttons.find('.on-readwrite').removeClass('hide');
                    } else {
                        this.viewManager.$buttons.find('.on-readwrite:not(.on-selected)').removeClass('hide');
                    }
                }
            },
        },
    });
    AnyBlokJS.register({
        classname: 'View.List.Line',
        extend: ['View.Entry'],
        prototype: {
            template: 'ViewListLine',
            init: function(view, record) {
                this._super(view, record);
                this.selected = false;
            },
            render: function () {
                var self = this;
                this._super();
                this.$el.find('input#line_checkbox').click(function () {
                    var nb = self.view.$el.find('input#line_checkbox:not(:checked)').length;
                    if (nb) {
                        self.view.$el.find('input#all_checkbox').prop('checked', false);
                    } else {
                        self.view.$el.find('input#all_checkbox').prop('checked', true);
                    }
                    if (self.$el.find('input#line_checkbox:checked').length) {
                        self.selected = true;
                    } else {
                        self.selected = false;
                    }
                    self.view.hide_show_buttons()
                })
                this.$el.find('td.selectable').click(function () {
                    if (self.view.readonly) {
                        self.view.transition('selectRecord', {id: self.id});
                    }
                });
            },
        },
    });
}) ();
