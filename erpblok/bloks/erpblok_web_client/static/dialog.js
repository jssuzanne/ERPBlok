(function () {
    var dialog_id = 0;
    function get_dialog_id() {
        dialog_id ++;
        return dialog_id;
    }
    AnyBlokJS.register({
        classname: 'Dialog',
        extend: ['ActionInterface'],
        prototype: {
            init: function() {
                this._super();
                this.$el = $($.templates('#ERPBlokDialog').render({'id': get_dialog_id()}));
                this.$el.appendTo($('body'));
                this.elem = new Foundation.Reveal(this.$el);
            },
            set_title: function(title) {
                this.$el.find('h2.dialog-title').text(title);
            },
            set_html: function(html) {
                this.$el.find('div.dialog-content').html(html);
            },

            add_close_button: function() {
                var self = this;
                var $button = $($.templates('#ERPBlokDialogClose').render());
                $button.appendTo(this.$el.find('div.close-button'));
                $button.click(function (e) {
                    self.elem.close();
                });
            },
            open: function() {
                this.elem.open();
            },
            destroy: function () {
                setTimeout(function(){self.$el.remove()}, 1000);
            },
        },
    });
}) ();
