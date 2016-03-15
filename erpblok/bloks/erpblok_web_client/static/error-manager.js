(function () {
    AnyBlokJS.register({classname: 'ErrorManager', prototype: {
        init: function() {
            this.$el = $('#errormanager').find('div');
            this.modal = new Foundation.Reveal($('#errormanager'));
        },
        open: function(msg) {
            this.$el.children().remove();
            var $node = $('<div/>');
            $(msg).appendTo($node);
            $node.appendTo(this.$el);
            this.modal.open();
        },
    }});
}) ();
