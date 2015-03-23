ERPBlok.MenuManager = ERPBlok.Model.extend({
    init: function() {
        this.define_user_menu();
        this.define_quick_menu();
    },
    define_user_menu: function() {
        var self = this;
        this.userMenu = new ERPBlok.UserMenu();
        $("#dropdown-usermenu a").click(function(e) {
            var func = e.currentTarget.dataset.function;
            self.userMenu.call_function(func);
        });
    },
    define_quick_menu: function() {
        var self = this;
        this.quickMenu = new ERPBlok.QuickMenu();
        $("#dropdown-quickmenu a").click(function(e) {
            var func = e.currentTarget.dataset.function;
            self.userMenu.call_function(func);
        });
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
});
ERPBlok.UserMenu = ERPBlok.MixinMenu.extend({
    do_about: function() {
        $.ajax({type: "POST",
                url: "/about",
                data: {}})
        .done(function (dialog) {
            $(dialog).dialog({
                appendTo: "body",
                dialogClass: "no-close",
                model: true,
                closeOnEscape: false,
                draggable: false,
                title: 'About',
                buttons: [
                    {text: "Close",
                     click: function() {$(this).dialog( "close" );}
                    },
                ],
            });
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
ERPBlok.Menu = ERPBlok.MixinMenu.extend({
    'rpc_url': '/web/client/menus',
});
