ERPBlok.ActionInterface = ERPBlok.Model.extend({
    appendTo: function (action) {
        console.error('appendTo function must be overloaded');
    },
    select_view: function (view, pks) {
        console.error('select_view function must be overloaded');
    },
    update_hash: function (kwargs) {
        console.error('update_hash function must be overloaded');
    },
    get_hash: function (key) {
        console.error('get_hash function must be overloaded');
    },
    reload: function (keephash) {
        if (keephash) {
            location.reload(true)
        } else {
            window.location = '/web/client';
        }
    },
    get_entries_values: function (values) {
        return values;
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
    select_view: function(view, kwargs) {
        if (kwargs != undefined && kwargs.id != undefined) {
            this.breadcrumb.update_last_hashtag({view: view,
                                                 pks: JSON.stringify(kwargs.id)});
        } else {
            this.breadcrumb.update_last_hashtag({view: view, pks: undefined});
        }
    },
    update_hash: function (kwargs) {
        this.breadcrumb.update_last_hashtag(kwargs);
    },
    get_hash: function (key) {
        return ERPBlok.hashTagManager.get(key);
    },
});
ERPBlok.Action = ERPBlok.Model.extend({
    'rpc_url': '/web/client/action',
    init: function(parent) {
        this.actionManager = parent || ERPBlok.actionManager;
        this.Dialog = ERPBlok.Dialog;
    },
    load: function(action, view_id, pks) {
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
        var viewManager = new ERPBlok.ViewManager(this, view_id, pks);
    },
});
