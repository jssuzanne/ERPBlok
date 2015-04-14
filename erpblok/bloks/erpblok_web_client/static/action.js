ERPBlok.ActionInterface = ERPBlok.Model.extend({
    appendTo: function (action) {
        console.error('appendTo function must be overloaded');
    },
    select_view: function (view, pks) {
        console.error('select_view function must be overloaded');
    },
});
ERPBlok.ActionManager = ERPBlok.ActionInterface.extend({
    init: function() {
        this.breadcrumb = new ERPBlok.BreadCrumb(this);
        this.$el = $('#action-manager');
    },
    load: function(action) {
        var action = new ERPBlok.Action();
        action.load(action_id);
    },
    clear_all: function() {
        this.breadcrumb.clear_all();
    },
    appendTo: function (action) {
        action.$el.appendTo(this.$el);
        this.breadcrumb.add(action.value.id, action.value.label, action.$el);
    },
    select_view: function(view, pks) {
        if (pks) {
            this.breadcrumb.update_last_hashtag({view: view,
                                                 pks: JSON.stringify(pks)});
        } else {
            this.breadcrumb.update_last_hashtag({view: view, pks: undefined});
        }
    },
});
ERPBlok.Action = ERPBlok.Model.extend({
    'rpc_url': '/web/client/action',
    init: function() {
        this.actionManager = ERPBlok.actionManager;
        this.Dialog = ERPBlok.Dialog;
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
        this.value = action;
        this.$el = $(tmpl('ERPBlokAction', {'id': action.id}));
        if (action.dialog) {
            var parent = new this.Dialog();
        } else {
            var parent = this.actionManager;
        }
        parent.appendTo(this);
        var viewManager = new ERPBlok.ViewManager(this);
    },
});
