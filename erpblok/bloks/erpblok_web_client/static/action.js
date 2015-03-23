ERPBlok.ActionManager = ERPBlok.Model.extend({
    'rpc_url': '/web/client/action',
    init: function() {
        this.breadcrums = new ERPBlok.BreadCrums(this);
        this.$views = $("section#application div#views");
    },
    load: function(action) {
        var self = this;
        if ($.isNumeric(action)) {
            this.rpc('load', {'action': action}, function (realAction) {
                self.load(realAction);
            });
            return;
        }
        if (!action.views.length) {
            return;
        }
        if (action.dialog) {
            var $node = this.new_dialog(action.id, action.label, action.dialog_properties || {});
        } else {
            var $node = this.new_action(action.id, action.label);
        }
        var viewManager = new ERPBlok.ViewManager(action.model);
        viewManager.appendTo($node);
        for (var i in action.views) {
            viewManager.add(action.views[i]);
        }
        viewManager.select_view(action.views[0].id);
    },
    fill_template: function($node) {
    },
    clear_all: function() {
        this.breadcrums.clear_all();
    },
    new_action: function(id, label) {
        var $node = $('<section id="' + id + '" class="action-manager"></section>');
        this.fill_template($node);
        $node.appendTo(this.$views);
        this.breadcrums.add(id, label, $node);
        return $node;
    },
    new_dialog: function (id, label, dialog_properties) {
        var $node = $('<div id="' + id + '"></div>');
        this.fill_template($node);
        var conf = {
            appendTo: "body",
            dialogClass: dialog_properties.dialogClass || "no-close",
            model: dialog_properties.model || true,
            closeOnEscape: dialog_properties.model || false,
            draggable: dialog_properties.draggable || false,
            width: dialog_properties.width || 800,
            maxHeight: dialog_properties.maxHeight || 640,
            title: label,
            close: function( event, ui ) {
                // TODO add the possibility to do another action
                $(this).dialog('destroy').remove()
            },
            buttons: [
            //    {text: "Close",
            //     click: function() {$(this).dialog( "close" );}
            //    },
            ],
        };
        $node.dialog(conf);
        return $node
    },
});
