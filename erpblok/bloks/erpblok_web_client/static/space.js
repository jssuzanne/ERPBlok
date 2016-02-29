(function () {
    AnyBlokJS.register({classname: 'Space', extend: ['Template', 'RPC'], prototype: {
        rpc_url: '/client/space/menu',
        init: function(parent, options) {
            this.client = parent;
            this.options = options;
            if (options.menus.length != 0) {
                this.template = 'Space_' + options.menu_position + '_Menu';
            } else {
                this.template = 'Space_without_Menu';
            }
        },
        unload: function() {
            var $app = $('#app');
            $app.children().remove();
        },
        selectMenu: function (menu) {
        },
        load: function() {
            this.$el = this.render_template(this.options);
            this.actionManager = AnyBlokJS.new('ActionManager', this.client, this.$el);
            var $app = $('#app');
            this.$el.appendTo($app);
            if (this.options.menus.length != 0) {
                this.menu = ReactDOM.render(
                    <Menu menus={this.options.menus}
                          space={this.options.id}
                          select={this.selectMenu.bind(this)}/>,
                    this.$el.find('menu')[0]);
                this.Fel = new Foundation.AccordionMenu(this.$el);
                var menu = this.client.hashTagManager.get('menu'),
                    action = this.client.hashTagManager.get('action');
                if (!menu && this.options.default_menu) {
                    this.client.load_menu(menu);
                } else {
                    this.load_menu(menu);
                }
                this.callAction(action);
            }
        },
        load_menu: function (menu) {
            var self = this;
            if (this.client.hashTagManager.get('clean-breadcrumbs')) {
                this.client.hashTagManager.update({'clean-breadcrumbs': undefined});
                this.actionManager.clear_all();
            }
            this.rpc('openMenu', {menu: menu}, function (res) {
                self.collapse_all();
                self.uncollapse_menus(res.nodemenu);
                self.active_menu(res.activemenu);
                if (self.client.hashTagManager.get('breadcrumb')) {
                    self.client.hashTagManager.update({breadcrumb: undefined});
                    return;
                }
            });
        },
        uncollapse_menus: function(nodemenus) {
            for (var i in nodemenus) {
                this.Fel.down(this.$el.find('menu').find('ul.menu-' + nodemenus[i]));
            }
        },
        collapse_all: function () {
            this.Fel.hideAll();
            this.$el.find('menu').find('.is-active').removeClass('is-active');
        },
        active_menu: function(menu_id) {
            this.$el.find('menu').find('a#menu' + menu_id).addClass('is-active');
        },
        callAction: function(action_id) {
            var action = AnyBlokJS.new('Action', this.actionManager);
            action.load(action_id);
        },
    }});
}) ();
