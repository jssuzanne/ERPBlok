ERPBlok.MenuManager = ERPBlok.Model.extend({
    init: function() {
        this.define_user_menu();
        this.define_quick_menu();
        this.define_side_menu();
    },
    define_user_menu: function() {
        var self = this;
        this.userMenu = new ERPBlok.UserMenu();
        $("#dropdown-usermenu a").click(function(e) {
            self.on_click(e, self.userMenu);
        });
    },
    define_quick_menu: function() {
        var self = this;
        this.quickMenu = new ERPBlok.QuickMenu();
        $("#dropdown-quickmenu a").click(function(e) {
            self.on_click(e, self.quickMenu);
        });
    },
    define_side_menu: function() {
        var self = this;
        this.sideMenu = new ERPBlok.SideMenu();
        ERPBlok.hashTagManager.onAdd('menu', function(newMenu) {
            self.sideMenu.openMenu(newMenu);
        });
        ERPBlok.hashTagManager.onChange('menu', function(newMenu, oldMenu) {
            self.sideMenu.openMenu(newMenu);
        });
    },
    on_click: function(e, target) {
        var func = e.currentTarget.dataset.function;
        var action = e.currentTarget.dataset.action;
        if (func) target.call_function(func);
        if (action) target.call_action(action);
    },
});
ERPBlok.MixinMenu = ERPBlok.Model.extend({
    call_function: function(function_name) {
        if (this[function_name] != undefined) {
            this[function_name]();
        } else {
            console.error("Unknown function : " + function_name);
        }
    },
    call_action: function(action_id) {
        // FIXME action will be taken some args
        var action = new ERPBlok.Action();
        action.load(action_id);
    },
});
ERPBlok.UserMenu = ERPBlok.MixinMenu.extend({
    do_about: function() {
        $.ajax({type: "POST",
                url: "/about",
                data: {}})
        .done(function (dialog_html) {
            var dialog = new ERPBlok.Dialog();
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
});
ERPBlok.QuickMenu = ERPBlok.MixinMenu.extend({});
ERPBlok.SideMenu = ERPBlok.MixinMenu.extend({
    'rpc_url': '/web/client/side/menu',
    init: function () {
        this.$el = $('.slide-out');
    },
    openMenu: function(newMenu) {
        var self = this;
        if (ERPBlok.hashTagManager.get('breadcrumb')) {
            ERPBlok.hashTagManager.update({breadcrumb: undefined});
            return;
        }
        if (ERPBlok.hashTagManager.get('clean-breadcrumbs')) {
            ERPBlok.hashTagManager.update({'clean-breadcrumbs': undefined});
            ERPBlok.actionManager.clear_all();
        }
        this.rpc('openMenu', {menu: newMenu}, function (res) {
            self.$el.find('.active').removeClass('active');
            self.uncollapse_menus(res.nodemenu);
            self.active_menu(res.activemenu);
            var func = res.function;
            var action = res.action;
            if (func) self.call_function(func);
            if (action) self.call_action(action);
        });
    },
    uncollapse_menus: function(nodemenus) {
        for (var i in nodemenus) {
            this.$el.find('div#menu' + nodemenus[i] + '.content').addClass('active');
            this.$el.find('a#amenu' + nodemenus[i]).addClass('active');
        }
    },
    active_menu: function(menu_id) {
        this.$el.find('a#menu' + menu_id + '.side-menu').addClass('active');
    },
});
