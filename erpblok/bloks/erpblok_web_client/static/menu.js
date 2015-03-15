ERPBlok.Menu = ERPBlok.Model.extend({
    call_function: function(function_name) {
        if (this[function_name] != undefined) {
            this[function_name]();
        } else {
            console.error("Unknown function : " + function_name);
        }
    },
});
ERPBlok.UserMenu = ERPBlok.Menu.extend({
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
ERPBlok.QuickMenu = ERPBlok.Menu.extend({});
ERPBlok.Menus = ERPBlok.Menu.extend(ERPBlok.RPC.prototype, {
    'rpc_url': '/web/client/menus',
});
