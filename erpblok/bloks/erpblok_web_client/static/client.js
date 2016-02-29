(function () {
    AnyBlokJS.register({classname: 'Client', extend: ['Template'], prototype: {
        template: 'Client',
        init: function () {
            this.init_foundation();
            this.hashTagManager = AnyBlokJS.new('HashTagManager', this);
            this.errorManager = AnyBlokJS.new('ErrorManager', this);
            var self = this;
            this.hashTagManager.onAdd('space', function(newSpace) {self.selectLeftMenu(newSpace);});
            this.hashTagManager.onChange('space', function(newSpace, oldSpace) {self.selectLeftMenu(newSpace);});
            this.hashTagManager.onAdd('menu', function(newMenu) {self.selectMenu(newMenu);});
            this.hashTagManager.onChange('menu', function(newMenu, oldMenu) {self.selectMenu(newMenu);});
        },
        init_foundation: function () {
            this.leftModal = new Foundation.Reveal($('#revealtopbarleft'));
            this.rightModal = new Foundation.Reveal($('#revealtopbarright'));
        },
        load: function () {
            var self = this;
            $.ajax({type: 'POST',
                    url: '/client/user/description'}).done(function (user) {
                self.load_left_reveal(user)
                self.load_right_reveal(user)
                self.hashTagManager.changed(self.hashTagManager.toObject(window.location.hash), {});
            });
        },
        selectMenu: function (menu) {
            if (this.current_space) {
                this.current_space.load_menu(menu);
            }
        },
        callAction: function (action) {
            if (this.current_space) {
                this.current_space.callAction(action);
            }
        },
        load_menu: function (menu) {
            this.hashTagManager.update({menu: menu});
        },
        closeLeftRemoval: function () {
            this.leftModal.close();
        },
        selectLeftMenu: function (value) {
            this.closeLeftRemoval();
            this.hashTagManager.update({space: value});
            var self = this;
            $.ajax({type: 'POST', url: '/client/space/description?space=' + value})
            .fail(function (xhr, status) {
                self.errorManager.open(xhr.responseText);
            })
            .done(function (space) {
                self.leftrevealButton.setState({icon: space.icon, label: space.label});
                if (self.current_space) {
                    self.current_space.unload();
                }
                self.current_space = AnyBlokJS.new('Space', self, space);
                self.current_space.load();
            });
        },
        openLeftReveal: function (menuname) {
            var self = this;
            $.ajax({type: 'POST',
                    url: '/client/space/menus'}).done(function (menus) {
                self.leftrevealModal.setState({menus: menus});
                self.leftModal.open();
            });
        },
        load_left_reveal: function (user) {
            this.leftrevealButton = ReactDOM.render(
                <MenuRevealButton label="Selected space => "
                                  click={this.openLeftReveal.bind(this)}/>,
                document.getElementById('topbarleft'));
            this.leftrevealModal = ReactDOM.render(
                <MenuRevealModal select={this.selectLeftMenu.bind(this)}
                                 close={this.closeLeftRemoval.bind(this)} />,
                document.getElementById('revealtopbarleft'));
            if (user.space) {
                this.selectLeftMenu(user.space);
            }
        },
        closeRightRemoval: function () {
            this.rightModal.close();
        },
        selectRightMenu: function (value) {
            this.closeRightRemoval();
            this[value]();
        },
        openRightReveal: function (menuname) {
            var self = this;
            $.ajax({type: 'POST',
                    url: '/client/user/menus'}).done(function (menus) {
                self.rightrevealModal.setState({menus: menus});
                self.rightModal.open();
            });
        },
        load_right_reveal: function (user) {
            this.rightrevealButton = ReactDOM.render(
                // TODO put image
                <MenuRevealButton label={user.label}
                                  click={this.openRightReveal.bind(this)}/>,
                document.getElementById('topbarright'));
            this.rightrevealModal = ReactDOM.render(
                <MenuRevealModal select={this.selectRightMenu.bind(this)}
                                 close={this.closeRightRemoval.bind(this)} />,
                document.getElementById('revealtopbarright'));
        },
        return_to_login_page: function() {
            $.ajax({type: "POST",
                    url: "/login/disconnect",
                    data: {}})
            .done(function (url) {
                window.location = url;
            });
        },
    }});
}) ();
