(function () {

    ERPBlok.declare_react_class('Field')
    AnyBlokJS.register({classname: 'Field', prototype: {
        render_field_fake: function () {
            return this.render_field_String();
        },
        render_field_String: function () {
            return <FieldString options={this.props.options}
                                pressEnter={this.props.pressEnter}
                                init_field={this.props.init_field}
                                is_readonly={this.props.is_readonly}
                                get_value_of={this.props.get_value_of}
                                update_field={this.props.update_field} />
        },
        render_field_Integer: function () {
            return <FieldInteger options={this.props.options}
                                 pressEnter={this.props.pressEnter}
                                 init_field={this.props.init_field}
                                 is_readonly={this.props.is_readonly}
                                 get_value_of={this.props.get_value_of}
                                 update_field={this.props.update_field} />
        },
        render_field_Boolean: function () {
            return <FieldBoolean options={this.props.options}
                                 pressEnter={this.props.pressEnter}
                                 init_field={this.props.init_field}
                                 is_readonly={this.props.is_readonly}
                                 get_value_of={this.props.get_value_of}
                                 update_field={this.props.update_field} />
        },
        render_field_Float: function () {
            return <FieldFloat options={this.props.options}
                               pressEnter={this.props.pressEnter}
                               init_field={this.props.init_field}
                               is_readonly={this.props.is_readonly}
                               get_value_of={this.props.get_value_of}
                               update_field={this.props.update_field} />
        },
        render_field_Selection: function () {
            return <FieldSelection options={this.props.options}
                                   pressEnter={this.props.pressEnter}
                                   init_field={this.props.init_field}
                                   is_readonly={this.props.is_readonly}
                                   get_value_of={this.props.get_value_of}
                                   update_field={this.props.update_field} />
        },
        render_field_Password: function () {
            return <FieldPassword options={this.props.options}
                                  pressEnter={this.props.pressEnter}
                                  init_field={this.props.init_field}
                                  is_readonly={this.props.is_readonly}
                                  get_value_of={this.props.get_value_of}
                                  update_field={this.props.update_field} />
        },
        render_field_LargeBinary: function () {
            return <FieldLargeBinary options={this.props.options}
                                     pressEnter={this.props.pressEnter}
                                     init_field={this.props.init_field}
                                     is_readonly={this.props.is_readonly}
                                     get_value_of={this.props.get_value_of}
                                     update_field={this.props.update_field} />
        },
        render_field_Picture: function () {
            return <FieldPicture options={this.props.options}
                                 pressEnter={this.props.pressEnter}
                                 init_field={this.props.init_field}
                                 is_readonly={this.props.is_readonly}
                                 get_value_of={this.props.get_value_of}
                                 update_field={this.props.update_field} />
        },
        render_field_Many2One: function () {
            return <FieldMany2One options={this.props.options}
                                  pressEnter={this.props.pressEnter}
                                  init_field={this.props.init_field}
                                  is_readonly={this.props.is_readonly}
                                  get_value_of={this.props.get_value_of}
                                  update_field={this.props.update_field} />
        },
        render_field_One2One: function () {
            return <FieldOne2One options={this.props.options}
                                 pressEnter={this.props.pressEnter}
                                 init_field={this.props.init_field}
                                 is_readonly={this.props.is_readonly}
                                 get_value_of={this.props.get_value_of}
                                 update_field={this.props.update_field} />
        },
        render_field_Many2ManyChoices: function () {
            return <FieldMany2ManyChoices options={this.props.options}
                                          pressEnter={this.props.pressEnter}
                                          init_field={this.props.init_field}
                                          is_readonly={this.props.is_readonly}
                                          get_value_of={this.props.get_value_of}
                                          update_field={this.props.update_field} />
        },
        render: function () {
            var fnct_name = 'render_field_' + (this.props.options.type || 'fake');
            if (this[fnct_name]) {
                return this[fnct_name]();
            } else {
                console.log(fnct_name)
                return this.render_field_fake();
            }
        },
    }});

    ERPBlok.declare_react_class('FieldString')
    AnyBlokJS.register({classname: 'FieldString', prototype: {
        input_type: "text",
        getInitialState: function () {
            this.props.init_field(this.props.options.id, this);
            return {value: this.props.options.value,
                    readonly: this.props.is_readonly(this.props.options.id)};
        },
        handleChange: function (event) {
            this.props.update_field(this.props.options.id, event.target.value);
        },
        render_ro: function () {
            return <span>{this.state.value}</span>
        },
        get_style: function () {
            var style = {};
            if (! this.props.options.nullable) {
                style['background-color'] = 'lightblue';
                if (!this.state.value) {
                    style['border'] = '3px solid red';
                }
            }
            return style;
        },
        get_className: function () {
            var className='';
            if (!this.props.options.nullable) {
                if (!this.state.value) {
                    className = 'fieldNotNull fieldEmpty'
                } else {
                    className = 'fieldNotNull'
                }
            }
            return className
        },
        onKeyPress: function (event) {
            if (this.props.pressEnter && event.key == 'Enter') {
                this.props.pressEnter();
            }
        },
        render_rw: function () {
            var required = this.props.options.nullable ? false : true,
                placeholder = this.props.options.placeholder || '';
            return <input type={this.input_type}
                          required={required}
                          placeholder={placeholder}
                          value={this.state.value}
                          style={this.get_style()}
                          onKeyPress={this.onKeyPress.bind(this)}
                          onChange={this.handleChange.bind(this)}
                    />
        },
        render: function () {
            if (this.state.readonly) {
                return this.render_ro()
            } else {
                return this.render_rw()
            }
        },
    }});

    ERPBlok.declare_react_class('FieldSelection')
    AnyBlokJS.register({classname: 'FieldSelection', extend: ['FieldString'], prototype: {
        render_ro: function () {
            var value = this.state.value,
                self = this;
            this.props.options.selections.forEach(function (selection) {
                if (selection[0] == self.state.value) value = selection[1];
            });
            return <span>{value}</span>
        },
        render_rw: function () {
            var options = [];
            this.props.options.selections.forEach(function (selection) {
                options.push(<option value={selection[0]}>{selection[1]}</option>)
            });
            return (<select value={this.state.value}
                            className={this.get_className()}
                            onChange={this.handleChange.bind(this)} >
                        {options}
                    </select>)
        },
    }});

    ERPBlok.declare_react_class('FieldPassword')
    AnyBlokJS.register({classname: 'FieldPassword', extend: ['FieldString'], prototype: {
        input_type: 'password',
        render_ro: function () {
            return <span>******</span>
        },
    }});

    ERPBlok.declare_react_class('FieldInteger')
    AnyBlokJS.register({classname: 'FieldInteger', extend: ['FieldString'], prototype: {
        input_type: 'number',
        get_step: function () {
            return '1';
        },
        render_rw: function () {
            var required = this.props.options.nullable ? false : true,
                step = this.get_step();
            return <input type={this.input_type}
                          required={required}
                          value={this.state.value}
                          style={this.get_style()}
                          step={step}
                          onKeyPress={this.onKeyPress.bind(this)}
                          onChange={this.handleChange.bind(this)}
                    />
        },
    }});

    ERPBlok.declare_react_class('FieldFloat')
    AnyBlokJS.register({classname: 'FieldFloat', extend: ['FieldInteger'], prototype: {
        get_step: function () {
            return this.props.options.precision || '0.01';
        },
    }});

    ERPBlok.declare_react_class('FieldLargeBinary')
    AnyBlokJS.register({classname: 'FieldLargeBinary', extend: ['FieldString'], prototype: {
        input_type: 'file',
        handleChange: function (event) {
            var file = event.target.files[0],
                file_name = file.name,
                file_size = file.size,
                file_type = file.type;
            this.props.update_field(this.props.options.id, file);
            if (this.props.options.file_name_field)
                this.props.update_field(this.props.options.file_name_field, file_name);
            if (this.props.options.file_size_field)
                this.props.update_field(this.props.options.file_size_field, file_size);
            if (this.props.options.mimetype_field)
                this.props.update_field(this.props.options.mimetype_field, file_type);
        },
        onClick: function (event) {
            var image_data = atob(this.state.value.split(',')[1]);
            var arraybuffer = new ArrayBuffer(image_data.length);
            var view = new Uint8Array(arraybuffer);
            for (var i=0; i<image_data.length; i++) {
                view[i] = image_data.charCodeAt(i) & 0xff;
            }
            var mimetype = 'application/octet-stream';
            if (this.props.options.mimetype_field)
                mimetype = this.props.get_value_of(this.props.options.mimetype_field);

            var blob = new Blob([arraybuffer], {type: mimetype});
            var url = (window.webkitURL || window.URL).createObjectURL(blob);
            window.open(url);
        },
        get_title: function() {
            var txt = '';
            if (this.state.value) {
                txt = 'Download file';
                if (this.props.options.file_name_field) {
                    txt += ' : ' + this.props.get_value_of(this.props.options.file_name_field);
                    if (this.props.options.file_size_field) {
                        txt += ' (' + this.props.get_value_of(this.props.options.file_size_field) + ' bytes)';
                    }
                }
            }
            return txt
        },
        render_ro: function () {
            var txt = this.get_title();
            return <a onClick={this.onClick.bind(this)}>{txt}</a>
        },
        render_rw: function () {
            var required = this.props.options.nullable ? false : true,
                placeholder = this.props.options.placeholder || '',
                accept = this.props.options.accept || "*";
            return <input type={this.input_type}
                          required={required}
                          placeholder={placeholder}
                          value={this.state.value}
                          style={this.get_style()}
                          onKeyPress={this.onKeyPress.bind(this)}
                          onChange={this.handleChange.bind(this)}
                          accept={accept}
                    />
        },
    }});

    ERPBlok.declare_react_class('FieldPicture')
    AnyBlokJS.register({classname: 'FieldPicture',
                        extend: ['FieldLargeBinary'],
                        prototype: {
        render_ro: function () {
            var txt = this.get_title();
            return <img title={txt} src={this.state.value}/>
        },
    }});

    ERPBlok.declare_react_class('FieldBoolean')
    AnyBlokJS.register({classname: 'FieldBoolean', prototype: {
        getInitialState: function () {
            this.props.init_field(this.props.options.id, this);
            return {value: this.props.options.value,
                    readonly: this.props.is_readonly(this.props.options.id)};
        },
        handleChange: function (event) {
            this.props.update_field(this.props.options.id, event.target.checked);
        },
        render_ro: function () {
            return <input type="checkbox"
                          disabled
                          checked={this.state.value} />
        },
        render_rw: function () {
            return (
                    <input type="checkbox"
                           id={this.props.options.id}
                           onChange={this.handleChange.bind(this)}
                           checked={this.state.value} />)
        },
        render: function () {
            if (this.state.readonly) {
                return this.render_ro()
            } else {
                return this.render_rw()
            }
        },
    }});

    ERPBlok.declare_react_class('FieldMany2One')
    AnyBlokJS.register({classname: 'FieldMany2One',
                        extend: ['RPC'],
                        prototype: {
        rpc_url: '/web/client/field',
        getInitialState: function () {
            this.props.init_field(this.props.options.id, this);
            return {value: this.props.options.value,
                    choices: [],
                    label: 'Plop',
                    readonly: this.props.is_readonly(this.props.options.id)};
        },
        setState: function (states) {
            if ('value' in states) {
                if (JSON.stringify(this.state.value) != JSON.stringify(states.value)) {
                    var self = this;
                    this.rpc('x2One_render', {model: this.props.options.model,
                                              primary_keys: states.value}, function (label) {
                        self.setState({'label': label})
                    });
                }
            }
            this._super(states)
        },
        updateLabel: function () {
        },
        onClick: function (event) {
            if (this.state.value) {
                var action = AnyBlokJS.new('Action', this.props.options.actionManager);
                action.load(this.props.options.action,
                            this.props.options.action.selected,
                            JSON.stringify(this.state.value));
            }
        },
        render_ro: function() {
            return <a onClick={this.onClick.bind(this)}>{this.state.label}</a>
        },
        render_rw: function() {
            return <a onClick={this.onClick.bind(this)}>{this.state.label}</a>
        },
        render: function () {
            if (this.state.readonly) {
                return this.render_ro()
            } else {
                return this.render_rw()
            }
        },
    }});

    ERPBlok.declare_react_class('FieldOne2One')
    AnyBlokJS.register({classname: 'FieldOne2One',
                        extend: ['RPC', 'FieldMany2One'],
                        prototype: {
        setState: function (states) {
            if ('value' in states) {
                if (JSON.stringify(this.state.value) != JSON.stringify(states.value)) {
                    var self = this;
                    this.rpc('x2One_render', {model: this.props.options.model,
                                              primary_keys: states.value}, function (label) {
                        self.setState({'label': label})
                    });
                }
            }
            this._super(states)
        },
    }});

    ERPBlok.declare_react_class('FieldMany2ManyChoices')
    AnyBlokJS.register({classname: 'FieldMany2ManyChoices',
                        extend: ['RPC'],
                        prototype: {
        rpc_url: '/web/client/field',
        getInitialState: function () {
            this.props.init_field(this.props.options.id, this);
            return {value: this.props.options.value,
                    choices: [],
                    readonly: this.props.is_readonly(this.props.options.id)};
        },
        componentDidMount: function() {
            var self = this;
            this.rpc('get_RelationShip_entries', {model: this.props.options.model,
                                                  display: this.props.options.display}, function (result) {
                self.setState({choices: result});
            });
        },
        containsEntry : function(obj) {
            for (var x in this.state.value) {
                if (this.state.value.hasOwnProperty(x) && JSON.stringify(this.state.value[x]) === JSON.stringify(obj)) {
                    return x;
                }
            }
            return false;
        },
        render: function () {
            var choices = [],
                self = this,
                disabled = (this.state.readonly) ? true : false,
                large_up = 'large-up-' + (this.props.options.largegrid || 4),
                medium_up = 'medium-up-' + (this.props.options.mediumgrid || 2),
                small_up = 'small-up-' + (this.props.options.smallgrid || 1),
                className = 'row ' + large_up + ' ' + medium_up + ' ' + small_up;

            this.state.choices.forEach(function (choice) {
                var checked = false;
                if (self.containsEntry(choice[0])) checked = true;
                var onClick = function (event) {
                    if (event.target.checked) {
                        if (! self.containsEntry(choice[0]))
                            self.state.value.push(choice[0]);
                    } else {
                        var index = self.containsEntry(choice[0]);
                        self.state.value.splice(index, 1)
                    }
                    self.props.update_field(self.props.options.id, self.state.value);
                }
                choices.push(
                    <div className="columns">
                        <input type="checkbox"
                               checked={checked}
                               disabled={disabled}
                               onClick={onClick}/>
                        <label>{choice[1]}</label>
                    </div>)
            });
            return (<fieldset className="fieldset">
                        <legend>
                            <h6>
                                {this.props.options.label}
                            </h6>
                        </legend>
                        <div className={className}>
                            {choices}
                        </div>
                    </fieldset>)
        },
    }});
}) ();
