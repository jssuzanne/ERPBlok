ERPBlok.ViewManager = ERPBlok.Model.extend({
    init: function(action) {
        this.action = action;
        this.$action = action.$el;
        this.$selector = $(tmpl('ERPBlokViewManager', {}));
        this.$selector.appendTo(action.$el);
        this.views = {};
        this.active_view = undefined;
        for (var i in action.value.views) {
            this.add(action.value.views[i]);
        }
        var view_id = ERPBlok.hashTagManager.get('view');
        if (view_id) {
            var pks = ERPBlok.hashTagManager.get('pks');
            if (pks) {
                pks = JSON.parse(pks);
                this.select_view(view_id, pks);
            } else {
                this.select_view(view_id);
            }
        } else {
            this.select_view(action.value.selected);
        }
    },
    add: function(view) {
        var self = this;
        var view = this.get_view_cls(view);
        var $navEl = view.getNavEl();
        $navEl.click(function (event) {
            self.select_view(event.currentTarget.id);
        });
        $navEl.appendTo(this.$selector.find('ul'));
        var $viewEl = view.getViewEl();
        $viewEl.addClass('hide');
        $viewEl.appendTo(this.$action);
        this.views[view.options.id] = {
            '$nav': $navEl,
            '$view': $viewEl,
            'view': view
        };
    },
    get_view_cls: function(view) {
        if (ERPBlok.View[view.mode])
            return new ERPBlok.View[view.mode](this, view);
        return new ERPBlok.View(this, view);
    },
    select_view: function (view_id, kwargs) {
        if (view_id == this.active_view) return;
        if (this.active_view) {
            this.views[this.active_view].$nav.removeClass('active');
            this.views[this.active_view].$view.addClass('hide');
        }
        if (view_id) {
            this.active_view = view_id;
            this.views[view_id].$nav.addClass('active');
            this.views[view_id].$view.removeClass('hide');
            this.views[view_id].view.render(kwargs);
            this.action.actionManager.select_view(view_id, kwargs);
        }
    },
});
ERPBlok.View = ERPBlok.Model.extend({
    rpc_url: '/web/client/view',
    icon_selector: 'fi-alert',
    title_selector: 'undefined',
    class_name: 'view-undefined',
    init: function(viewManager, options) {
        this.viewManager = viewManager;
        this.options = options;
    },
    getNavEl: function(view_id) {
        return $(tmpl('ERPBlokViewSelector',
                      {'id': this.options.id,
                       'title_selector': this.title_selector,
                       'icon_selector': this.icon_selector,
                       'selectable': this.options.selectable}));
    },
    getViewEl: function() {
        var $el = $(tmpl('ERPBlokView',
                    {id: this.options.id, class_name: this.class_name}));
        if (this.options.template) $(this.options.template).appendTo($el);
        this.$el = $el;
        return $el;
    },
    render: function() {
    },
    transition: function(name, kwargs) {
        this['transition_' + name](kwargs);
    },
    transition_selectRecord: function(kwargs) {
        var selectRecord = this.options.transitions.selectRecord;
        if (selectRecord[0] == 'open_view') {
            this.viewManager.select_view(selectRecord[1], kwargs);
        }
    },
    get_field_cls: function(type) {
        if (ERPBlok.View.Field[type])
            return new ERPBlok.View.Field[type]();
        return new ERPBlok.View.Field();
    },
});
