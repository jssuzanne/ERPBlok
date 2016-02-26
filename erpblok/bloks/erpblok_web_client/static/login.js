(function () {
    AnyBlokJS.register({classname: 'Client', extend: ['Template'], prototype: {
        template: 'Client',
        init: function () {
            this.UrlSearchManager = AnyBlokJS.new('UrlSearchManager');
            this.init_foundation();
            this.fields = {
                login: {
                    id: 'login',
                    type: 'String',
                    nullable: true,
                    placeholder: 'Enter your login ...',
                    value: '',
                },
                password: {
                    id: 'password',
                    type: 'Password',
                    nullable: true,
                    placeholder: 'Enter the associated password ...',
                    value: '',
                },
            };
        },
        init_foundation: function () {
            this.leftModal = new Foundation.Reveal($('#revealtopbarleft'));
        },
        load: function () {
            this.load_auth();
            this.load_db_selector();
        },
        closeRemoval: function () {
            this.leftModal.close();
        },
        fnct_manage_db: function () {
            window.location = '/database/manager';
        },
        selectDB: function (value) {
            this.closeRemoval();
            this.$el.find('#error').addClass("hide");
            var fnct = 'fnct_' + value;
            if (this[fnct]) {
                this[fnct]();
            } else {
                this.revealButton.setState({icon: 'fi-database', label: value});
                this.database = value;
            }
        },
        openReveal: function (menuname) {
            var self = this;
            $.ajax({type: 'GET',
                    url: '/login/databases'}).done(function (menus) {
                self.revealModal.setState({menus: menus});
                self.leftModal.open();
            });
        },
        load_db_selector: function () {
            this.revealButton = ReactDOM.render(
                <MenuRevealButton label="Selected database => "
                                  click={this.openReveal.bind(this)}/>,
                document.getElementById('topbarleft'));
            this.revealModal = ReactDOM.render(
                <MenuRevealModal select={this.selectDB.bind(this)}
                                 close={this.closeRemoval.bind(this)} />,
                document.getElementById('revealtopbarleft'));
            var default_db = this.UrlSearchManager.get('database');
            if (default_db) {
                this.selectDB(default_db);
            }
        },
        initField: function (fieldname, instance) {
            this.fields[fieldname].instance = instance;
        },
        updateField: function (fieldname, value) {
            this.fields[fieldname].value = value;
            this.fields[fieldname].instance.setState({value: value});
        },
        isReadonly: function (fieldname) {
            return false;
        },
        add_error: function (msg) {
            var $error = this.$el.find('#error'),
                $node = $('<div>' + msg + '</div>');
            $error.removeClass("hide");
            $error.children().remove();
            $node.appendTo($error);
        },
        load_auth: function () {
            var $el = this.render_template();
            this.$el = $el;
            $el.appendTo($('#app'));
            for (var field in this.fields) {
                ReactDOM.render(<Field options={this.fields[field]}
                                       init_field={this.initField.bind(this)}
                                       is_readonly={this.isReadonly.bind(this)}
                                       update_field={this.updateField.bind(this)} />,
                                $el.find('field#' + field)[0]);
            }
            var self = this,
                hash = window.location.hash;
            $el.find('#submit').click(function (event) {
                var
                    database = self.database,
                    login = self.fields.login.value,
                    password = self.fields.password.value;
                if (database && login && password) {
                    $.ajax({type: "POST",
                            url:"/login/connect",
                            data: {database: database, login: login, password: password}})
                    .fail(function (xhr, status) {
                        if (xhr.status == 401) {
                            self.add_error('Wrong Login or Password');
                        } else {
                            self.add_error('Unknown error');
                        }
                    })
                    .done(function (url) {
                        window.location = url + hash;
                    });
                } else {
                    if (! database) {
                        self.add_error('Miss database');
                    }
                }
            });
        },
    }});
}) ();
