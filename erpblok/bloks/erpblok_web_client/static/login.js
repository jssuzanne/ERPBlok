(function () {
    AnyBlokJS.register({classname: 'Client', extend: ['Template'], prototype: {
        template: 'Client',
        init: function () {
            this.init_foundation();
            this.fields = {
                login: {
                    id: 'login',
                    type: 'string',
                    nullable: false,
                    placeholder: 'Enter your login ...',
                    value: '',
                },
                password: {
                    id: 'password',
                    type: 'password',
                    nullable: false,
                    placeholder: 'Enter the associated password ...',
                    value: '',
                },
            };
            this.database = null
        },
        init_foundation: function () {
            this.leftModal = new Foundation.Reveal($('#revealtopbarleft'));
        },
        load: function () {
            this.load_db_selector();
            this.load_auth();
        },
        closeRemoval: function () {
            this.leftModal.close();
        },
        selectDB: function (value) {
            this.closeRemoval();
            this.revealButton.setState({label: value});
            this.database = value;
        },
        selectedDB: function () {
            return {
                icon: 'fi-database large',
                label: 'Select a database',
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
                <MenuRevealButton getter={this.selectedDB.bind(this)} 
                                  click={this.openReveal.bind(this)}/>,
                document.getElementById('topbarleft'));
            this.revealModal = ReactDOM.render(
                <MenuRevealModal select={this.selectDB.bind(this)}
                                 close={this.closeRemoval.bind(this)} />,
                document.getElementById('revealtopbarleft'));
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
            $error.children().remove()
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
                    var misseddata = []
                    if (! database) {
                        misseddata.push('Database');
                    }
                    if (! login) {
                        misseddata.push('Login');
                    }
                    if (! password) {
                        misseddata.push('Password');
                    }
                    self.add_error('Miss ' + misseddata.toString())
                }
            });
        },
    }});
}) ();
