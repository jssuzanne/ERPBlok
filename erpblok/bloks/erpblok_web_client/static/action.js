(function () {
    AnyBlokJS.register({
        classname: 'ActionInterface',
        prototype: {
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
        },
    });
    AnyBlokJS.register({
        classname: 'ActionManager',
        extend: ['ActionInterface'],
        prototype: {
            init: function(client, $el) {
                this.client = client;
                this.breadcrumb = AnyBlokJS.new('BreadCrumbManager', this, $el);
                this.$el = $el.find('#action-manager');
            },
            load: function(action_id) {
                var action = AnyBlokJS.new('Action');
                action.load(action_id);
            },
            clear_all: function() {
                this.breadcrumb.clear_all();
            },
            appendTo: function (action) {
                action.$el.appendTo(this.$el);
                this.breadcrumb.add(action);
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
                return this.client.hashTagManager.get(key);
            },
        },
    });
    AnyBlokJS.register({
        classname: 'Action',
        extend: ['Template', 'RPC'],
        prototype: {
            rpc_url: '/web/client/action',
            template: 'Action',
            init: function(actionManager) {
                this.actionManager = actionManager;
                this.Dialog = 'Dialog';
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
                this.$el = this.render_template({id: action.id});
                if (action.dialog) {
                    var parent = AnyBlokJS.new(this.Dialog);
                } else {
                    var parent = this.actionManager;
                }
                parent.appendTo(this);
                this.viewManager = AnyBlokJS.new('ViewManager', this, view_id, pks);
            },
        },
    });
}) ();
