(function () {
    AnyBlokJS.register({
        classname: 'MenuManager',
        prototype: {
            init: function(client) {
                this.client = client;
                this.define_user_menu();
                this.define_quick_menu();
                this.define_side_menu();
            },
            define_user_menu: function() {
                var self = this;
                this.userMenu = AnyBlokJS.new('UserMenu');
                $("#dropdown-usermenu a").click(function(e) {
                    self.on_click(e, self.userMenu);
                });
            },
            define_quick_menu: function() {
                var self = this;
                this.quickMenu = AnyBlokJS.new('QuickMenu');
                $("#dropdown-quickmenu a").click(function(e) {
                    self.on_click(e, self.quickMenu);
                });
            },
            define_side_menu: function() {
                var self = this;
                this.sideMenu = AnyBlokJS.new('SideMenu', this.client);
                this.client.hashTagManager.onAdd('menu', function(newMenu) {
                    self.sideMenu.openMenu(newMenu);
                });
                this.client.hashTagManager.onChange('menu', function(newMenu, oldMenu) {
                    self.sideMenu.openMenu(newMenu);
                });
            },
            on_click: function(e, target) {
                var func = e.currentTarget.dataset.function;
                var action = e.currentTarget.dataset.action;
                if (func) target.call_function(func);
                if (action) target.call_action(action);
            },
        },
    });
    AnyBlokJS.register({
        classname: 'MixinMenu',
        prototype: {
            call_function: function(function_name) {
                if (this[function_name] != undefined) {
                    this[function_name]();
                } else {
                    console.error("Unknown function : " + function_name);
                }
            },
            call_action: function(action_id) {
                // FIXME action will be taken some args
                var action = AnyBlokJS.new('Action');
                action.load(action_id);
            },
        },
    });
    AnyBlokJS.register({
        classname: 'UserMenu',
        extend: ['MixinMenu'],
        prototype: {
            do_about: function() {
                $.ajax({type: "POST",
                        url: "/about",
                        data: {}})
                .done(function (dialog_html) {
                    var dialog = AnyBlokJS.new('Dialog');
                    dialog.set_title('About');
                    dialog.set_html(dialog_html);
                    dialog.add_close_button();
                    dialog.open();
                });
            },
            do_logout: function() {
                $.ajax({type: "POST",
                        url: "/login/disconnect",
                        data: {}})
                .done(function (url) {
                    window.location = url;
                });
            },
        },
    });
    AnyBlokJS.register({
        classname: 'QuickMenu',
        extend: ['MixinMenu'],
        prototype: {},
    });
    AnyBlokJS.register({
        classname: 'SideMenu',
        extend: ['MixinMenu', 'RPC'],
        prototype: {
            'rpc_url': '/web/client/side/menu',
            init: function (client) {
                this.client = client;
                this.$el = $('.side-menu');
            },
            openMenu: function(newMenu) {
                var self = this;
                if (this.client.hashTagManager.get('clean-breadcrumbs')) {
                    this.client.hashTagManager.update({'clean-breadcrumbs': undefined});
                    this.client.actionManager.clear_all();
                }
                this.rpc('openMenu', {menu: newMenu}, function (res) {
                    self.collapse_all();
                    self.uncollapse_menus(res.nodemenu);
                    self.active_menu(res.activemenu);
                    if (self.client.hashTagManager.get('breadcrumb')) {
                        self.client.hashTagManager.update({breadcrumb: undefined});
                        return;
                    }
                    var func = res.function;
                    var action = res.action;
                    if (func) self.call_function(func);
                    if (action) self.call_action(action);
                });
            },
            collapse_all: function () {
                this.client.accordionMenuLarge.hideAll();
                this.client.accordionMenuSmall.hideAll();
                this.$el.find('.is-active').removeClass('is-active');
            },
            uncollapse_menus: function(nodemenus) {
                for (var i in nodemenus) {
                    this.client.accordionMenuLarge.down(this.$el.find('ul.side-menu-' + nodemenus[i]));
                }
            },
            active_menu: function(menu_id) {
                this.$el.find('a#menu' + menu_id).addClass('is-active');
            },
        },
    });
}) ();
