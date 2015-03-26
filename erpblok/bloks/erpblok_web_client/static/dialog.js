var dialog_id = 0;
function get_dialog_id() {
    dialog_id ++;
    return dialog_id;
}
ERPBlok.Dialog = ERPBlok.ActionInterface.extend({
    init: function() {
        var id = get_dialog_id();
        var modal = '<div id="modal' + id + '" class="modal">';
        modal += '<div class="modal-content">';
        modal += '<h4 class="dialog-title"></h4>';
        modal += '<div class="dialog-content"></div>';
        modal += '<div class="modal-footer"></div>';
        modal += '</div>';
        this.$el = $(modal);
        this.$el.appendTo($('body'));
    },
    set_title: function(title) {
        this.$el.find('h4.dialog-title').text(title);
    },
    set_html: function(html) {
        this.$el.find('div.dialog-content').html(html);
    },
    add_close_button: function() {
        var $button = $('<a class="waves-effect waves-green btn-flat modal-action modal-close">Close</a>');
        $button.appendTo(this.$el.find('div.modal-footer'));
    },
    open: function() {
        var self = this;
        this.$el.openModal({
            dismissible: false,
            complete: function () {
                self.$el.remove();
            },
        });
    },
});
