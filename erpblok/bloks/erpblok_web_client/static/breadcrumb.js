ERPBlok.BreadCrumb = ERPBlok.Model.extend({
    init: function(actionManager) {
        this.$el = $('div#breadcrumb');
        this.links = [];
        this.actionManager = actionManager;
        this.$last = undefined;
    },
    get_hashTag: function () {
        return $.extend({
            breadcrumb: true},
            ERPBlok.hashTagManager.toObject(window.location.hash));
    },
    add: function(id, label, $node) {
        var self = this;
        if (this.$last) {
            this.$last.link.removeClass('current');
            this.$last.link.click(function (e) {self.on_click(e);});
            this.$last.node.addClass('hide')
            this.links.push(this.$last);
        }
        // FIXME get the active menu and save it in last
        this.$last = {
            link: $(tmpl('ERPBlokBreadCrumb', {'id': id, 'label': label})),
            node: $node,
            hash: this.get_hashTag(),
        };
        this.$last.link.appendTo(this.$el);
    },
    update_last_hashtag: function(hash) {
        if (this.$last){
            this.$last.hash = $.extend({}, hash, this.$last.hash);
            ERPBlok.hashTagManager.update(hash);
        }
    },
    on_click: function (event) {
        this.$last.link.remove();
        this.$last.node.remove();
        var link = event.currentTarget;
        for (var i = this.links.length - 1; i >= 0; i--) {
            if (this.links[i].link[0] == link) {
                var $link = this.links[i].link,
                    $node = this.links[i].node,
                    hash = this.links[i].hash;
                $link.addClass('current');
                this.$last = this.links[i];
                $node.removeClass('hide');

                var delta = this.links.length - i;
                this.links.slice(i, delta);
                ERPBlok.hashTagManager.update(hash);
                // FIXME reactive the good menus
                break;
            } else {
                this.links[i].link.remove();
                this.links[i].node.remove();
            }
        }
    },
    clear_all: function () {
        $.each(this.links, function(i, item) {
            item.link.remove();
            item.node.remove();
        })
        this.links = [];
        if (this.$last) {
            this.$last.link.remove();
            this.$last.node.remove();
            this.$last = undefined;
        }
    },
});
