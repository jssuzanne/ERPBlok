ERPBlok.ActionManager = ERPBlok.Model.extend(ERPBlok.RPC.prototype, {
    'rpc_url': '/web/client/action',
    init: function() {
        this.breadcrums = new ERPBlok.BreadCrums();
        this.views = $("section#application div#views");
    },
    load: function(action) {
        var self = this;
        if ($.isNumeric(action)) {
            this.rpc('load', {'action': action}, function (realAction) {
                self.load(realAction);
            });
            return;
        }
    },
});
