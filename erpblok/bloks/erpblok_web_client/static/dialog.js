var dialog_id = 0;
function get_dialog_id() {
    dialog_id ++;
    return dialog_id;
}
ERPBlok.Dialog = ERPBlok.ActionInterface.extend({
    init: function() {
        this.$el = $(tmpl('ERPBlokDialog', {'id': get_dialog_id()}));
        this.$el.appendTo($('body'));
    },
    set_title: function(title) {
        this.$el.find('h2.dialog-title').text(title);
    },
    set_html: function(html) {
        this.$el.find('div.dialog-content').html(html);
    },

    add_close_button: function() {
        var self = this;
        var $button = $(tmpl('ERPBlokDialogClose', {}));
        $button.appendTo(this.$el.find('div.dialog-content'));
        $button.click(function (e) {
            self.$el.foundation('reveal', 'close');
            setTimeout(function(){self.$el.remove()}, 1000);
        });
    },
    open: function() {
        this.$el.foundation('reveal', 'open');
    },
});
