var dialog_id = 0;
function get_dialog_id() {
    dialog_id ++;
    return dialog_id;
}
ERPBlok.Dialog = ERPBlok.ActionInterface.extend({
    init: function() {
        var id = get_dialog_id();
        var modal = '<div id="modal' + id + '" class="reveal-modal">';
        modal += '<h2 class="dialog-title"></h2>';
        modal += '<div class="dialog-content"></div>';
        modal += '</div>';
        this.$el = $(modal);
        this.$el.appendTo($('body'));
        this.$el.foundation('reveal', {
            opened: function () {
                alert('The couch was stolen!');
            },
            closed: function () {
                alert("Now it's yours again");
            }
        });
    },
    set_title: function(title) {
        this.$el.find('h2.dialog-title').text(title);
    },
    set_html: function(html) {
        this.$el.find('div.dialog-content').html(html);
    },

    add_close_button: function() {
        var self = this;
        var $button = $('<a class="button">Close</a>');
        $button.appendTo(this.$el.find('div.dialog-content'));
        $button.click(function (e) {
            self.$el.foundation('reveal', 'close');
            self.$el.remove();
        });
    },
    open: function() {
        this.$el.foundation('reveal', 'open');
    },
});
