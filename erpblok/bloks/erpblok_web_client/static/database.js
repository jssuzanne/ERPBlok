(function () {
    AnyBlokJS.register({classname: 'Client', extend: ['Template'], prototype: {
        init: function () {
            this.init_foundation();
        },
        init_foundation: function () {
            this.leftModal = new Foundation.Reveal($('#revealtopbarleft'));
        },
        load: function () {
            this.load_page_selector();
        },
        closeRemoval: function () {
            this.leftModal.close();
        },
        selectMenu: function (value) {
            this.closeRemoval();
            this[value]();
        },
        openReveal: function (menuname) {
            var self = this;
            $.ajax({type: 'GET',
                    url: '/database/menus'}).done(function (menus) {
                self.revealModal.setState({menus: menus});
                self.leftModal.open();
            });
        },
        load_page_selector: function () {
            this.revealButton = ReactDOM.render(
                <MenuRevealButton label='Selected Menu => '
                                  click={this.openReveal.bind(this)}/>,
                document.getElementById('topbarleft'));
            this.revealModal = ReactDOM.render(
                <MenuRevealModal select={this.selectMenu.bind(this)}
                                 close={this.closeRemoval.bind(this)} />,
                document.getElementById('revealtopbarleft'));
            // this.open_create_page();
            this.open_drop_page();
        },
        return_to_login_page: function () {
            window.location = '/';
        },
        render_template: function(template, values={}) {
            this.template = template;
            var $el = this._super(values),
                $app = $('#app');

            $app.children().remove();
            // maybe drop also the react instance
            $el.appendTo($app);
            return $el
        },
        applyReactField: function ($el, fields){
            this.fields = fields;
            for (var field in this.fields) {
                ReactDOM.render(<Field options={this.fields[field]}
                                       init_field={this.initField.bind(this)}
                                       is_readonly={this.isReadonly.bind(this)}
                                       update_field={this.updateField.bind(this)} />,
                                $el.find('field#' + field)[0]);
            }
        },
        open_create_page: function() {
            this.revealButton.setState({icon: 'fi-plus', 
                                        label: 'Create a new database'});
            var self= this;
            $.ajax({type: 'GET',
                    url: '/database/addons'}).done(function (addons) {
                var $el = self.render_template('ClientCreateDB', {addons: addons});
                var fields = {
                    database: {
                        id: 'database',
                        type: 'String',
                        nullable: false,
                        placeholder: 'Enter the name of the database',
                        value: '',
                    },
                    login: {
                        id: 'login',
                        type: 'String',
                        nullable: false,
                        placeholder: 'Enter the login of the administrator',
                        value: '',
                    },
                    password: {
                        id: 'password',
                        type: 'Password',
                        nullable: false,
                        placeholder: 'Enter the associated password ...',
                        value: '',
                    },
                    password2: {
                        id: 'password2',
                        type: 'Password',
                        nullable: false,
                        placeholder: 'Confirm the associated password ...',
                        value: '',
                    },
                };
                for (var index in addons) {
                    var addon = addons[index];
                    fields[addon.id] = {
                        id: addon.id,
                        type: 'Boolean',
                        value: addon.value,
                    }
                }
                self.applyReactField($el, fields);
            });
        },
        open_drop_page: function() {
            this.revealButton.setState({icon: 'fi-trash', 
                                        label: 'Drop an existing database'});
            var $el = this.render_template('ClientDropDB');
            var self= this;
            $.ajax({type: 'GET',
                    url: '/database/selection'}).done(function (field) {
                var fields = {}
                fields[field.id] = field;
                self.applyReactField($el, fields);
            });
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
        /*
        load_auth: function () {
            var $el = this.render_template();
            this.$el = $el;
            $el.appendTo($('#app'));
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
        */
    }});
}) ();
