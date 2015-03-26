ERPBlok.BreadCrumb = ERPBlok.Model.extend({
    init: function(actionManager) {
        this.$el = $('main div#breadcrumb ul');
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
            var $last = this.$last.link,
                $last_node = this.$last.node,
                last_id = $last[0].id,
                last_label = $last[0].textContent,
                last_hash = this.$last.hash;
            $last.remove();
            var $link = $('<li class="link" id="' + last_id + '"><a>' + last_label + '</a></li>');
            $link.click(function (e) {self.on_click(e);});
            $link.appendTo(this.$el);
            $last_node.addClass('hide')
            this.links.push({'link': $link, 'node': $last_node, hash: last_hash});
        }
        this.$last = {
            link: $('<li class="last" id="' + id + '">' + label + '</li>'),
            node: $node,
            hash: this.get_hashTag(),
        };
        this.$last.link.appendTo(this.$el);
    },
    on_click: function (event) {
        this.$last.link.remove();
        this.$last.node.remove();
        var link = event.currentTarget;
        for (var i = this.links.length - 1; i >= 0; i--) {
            if (this.links[i].link[0] == link) {
                var id = this.links[i].link[0].id,
                    label = this.links[i].link.find('a')[0].textContent,
                    $node = this.links[i].node,
                    hash = this.links[i].hash;
                this.$last = {
                    'link': $('<li class="last" id="' + id + '">' + label + '</li>'),
                    'node': $node,
                };
                this.links[i].link.remove();
                $node.removeClass('hide');
                this.$last.link.appendTo(this.$el);
                var delta = this.links.length - i;
                this.links.slice(i, delta);
                ERPBlok.hashTagManager.update(hash);
                break;
            } else {
                this.links[i].link.remove();
                this.links[i].node.remove();
            }
        }
    },
    clear_all: function () {
        for (var i in this.links) {
            this.links[i].link.remove();
            this.links[i].node.remove();
        }
        this.links = [];
        if (this.$last) {
            this.$last.link.remove();
            this.$last.node.remove();
            this.$last = undefined;
        }
    },
});
