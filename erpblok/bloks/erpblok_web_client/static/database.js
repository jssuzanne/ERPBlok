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
            this.open_create_page();
        },
        return_to_login_page: function () {
            window.location = '/';
        },
        render_template: function(template, onClick, values={}) {
            this.template = template;
            var $el = this._super(values),
                self = this,
                $app = $('#app');

            $app.children().remove();
            // maybe drop also the react instance
            $el.appendTo($app);
            $el.find('a#submit').click(function (event) {
                if (self.validate_required_fields()) {
                    onClick($el);
                }
            });
            return $el
        },
        validate_required_fields: function () {
            var onErrorField = []
            for (var index in this.fields) {
                if (this.fields[index].nullable === false) {
                    if (!this.fields[index].value) {
                        onErrorField.push(this.fields[index].id);
                    }
                }
            }
            if (onErrorField.length != 0) {
                notify_error('Some fields miss',
                             'Please fill the fields : ' + onErrorField.toString())
                return false;
            }
            return true;
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
            var self= this,
                installable_bloks = [];
            var onClick = function ($el) {
                $el.find('.alert').addClass('hide');
                if (self.fields.password.value != self.fields.password2.value) {
                    $el.find('#error2').removeClass('hide');
                } else if (database && login && password) {
                    var install_bloks = [];
                    for (var index in installable_bloks) {
                        if (self.fields[installable_bloks[index]].value) {
                            install_bloks.push(installable_bloks[index]);
                        }
                    } 
                    $.ajax({type: "POST",
                            url:"/database/manager/create",
                            data: {database: self.fields.database.value, 
                                   login: self.fields.login.value, 
                                   password: self.fields.password.value,
                                   install_bloks: install_bloks.toString(),
                                   db_manager_password: self.fields.db_manager_password.value}})
                    .fail(function (xhr, status) {
                        if (xhr.status == 401) {
                            $el.find('#error3').removeClass("hide");
                        }
                        if (xhr.status == 403) {
                            $el.find('#error').removeClass("hide");
                        }
                    })
                    .done(function (url) {
                        window.location = url;
                    });
                }
            }
            $.ajax({type: 'GET',
                    url: '/database/addons'}).done(function (addons) {
                var $el = self.render_template('ClientCreateDB', onClick, {addons: addons});
                var fields = {
                    db_manager_password: {
                        id: 'db_manager_password',
                        type: 'Password',
                        nullable: false,
                        placeholder: 'Enter the administrator password ...',
                        value: '',
                    },
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
                    installable_bloks.push(addon.id);
                }
                self.applyReactField($el, fields);
            });
        },
        open_drop_page: function() {
            this.revealButton.setState({icon: 'fi-trash', 
                                        label: 'Drop an existing database'});
            var self= this;
            var onClick = function ($el) {
                $.ajax({type: "POST",
                        url:"/database/manager/drop",
                        data: {database: self.fields.database.value, 
                        db_manager_password:self.fields.db_manager_password.value}})
                .fail(function (xhr, status) {
                    if (xhr.status == 401) {
                        $el.find('#error').removeClass("hide");
                    }
                }).done (function () {
                    self.open_create_page();
                });
            }
            var $el = this.render_template('ClientDropDB', onClick);
            $.ajax({type: 'GET',
                    url: '/database/selection'}).done(function (field) {
                var fields = {
                    db_manager_password: {
                        id: 'db_manager_password',
                        type: 'Password',
                        nullable: false,
                        placeholder: 'Enter the administrator password ...',
                        value: '',
                    },
                }
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
    }});
}) ();
