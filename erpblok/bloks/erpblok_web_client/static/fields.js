(function () {

    ERPBlok.declare_react_class('Field')
    AnyBlokJS.register({classname: 'Field', prototype: {
        render: function () {
            var FieldType = ERPBlok.get_field_definition(this.props.options.type || 'String'),
                props = {
                    options: this.props.options,
                    pressEnter: this.props.pressEnter,
                    init_field: this.props.init_field,
                    is_readonly: this.props.is_readonly,
                    get_value_of: this.props.get_value_of,
                    update_field: this.props.update_field,
                };
            return React.createElement(FieldType, props);
        },
    }});

    var field_counter = 0;
    function get_field_counter () {return field_counter ++;}
    function check_eval (condition, fields) {return eval(condition);}

    AnyBlokJS.register({classname: 'BaseField', prototype: {
        getInitialState: function () {
            this.props.init_field(this.props.options.id, this);
            return {value: this.props.options.value,
                    all_fields_value: this.props.options.all_fields_value || {},
                    readonly: this.props.is_readonly(this.props.options.id)};
        },
        is_readonly: function() {
            if (this.state.readonly) return true;
            if (this.props.options['writable-only-if']) {
                if (!check_eval(this.props.options['writable-only-if'], this.state.all_fields_value))
                    return true;
            }
            return false;
        },
        is_visible: function() {
            if (this.props.options['visible-only-if']) {
                if (check_eval(this.props.options['visible-only-if'], this.state.all_fields_value))
                    return true;

                return false;
            }
            return true;
        },
        is_not_nullable: function() {
            if (!this.props.options.nullable) return true;
            if (this.props.options['not-nullable-only-if']) {
                if (check_eval(this.props.options['not-nullable-only-if'], this.state.all_fields_value))
                    return true;

            }
            return false;
        },
        render: function () {
            if (!this.is_visible()) return <div/>
            if (this.is_readonly()) {
                return this.render_ro()
            } else {
                return this.render_rw()
            }
        },
        get_style: function () {
            var style = {};
            if (this.is_not_nullable()) {
                style['background-color'] = 'lightblue';
                if (!this.state.value) {
                    style['border'] = '3px solid red';
                }
            }
            return style;
        },
        get_className: function () {
            var className='';
            if (this.is_not_nullable()) {
                if (!this.state.value) {
                    className = 'fieldNotNull fieldEmpty'
                } else {
                    className = 'fieldNotNull'
                }
            }
            return className
        },
        handleChange: function (event) {
            this.props.update_field(this.props.options.id, event.target.value);
        },
        onKeyPress: function (event) {
            if (this.props.pressEnter && event.key == 'Enter') {
                this.props.pressEnter();
            }
        },
    }});

    ERPBlok.declare_react_class('FieldString', 'String')
    AnyBlokJS.register({classname: 'FieldString',
                        extend: ['BaseField'],
                        prototype: {
        input_type: "text",
        render_ro: function () {
            return <span>{this.state.value}</span>
        },
        render_rw: function () {
            var placeholder = this.props.options.placeholder || '';
            return <input type={this.input_type}
                          required={this.is_not_nullable()}
                          placeholder={placeholder}
                          value={this.state.value}
                          style={this.get_style()}
                          onKeyPress={this.onKeyPress.bind(this)}
                          onChange={this.handleChange.bind(this)}
                    />
        },
    }});

    ERPBlok.declare_react_class('FieldSelection', 'Selection')
    AnyBlokJS.register({classname: 'FieldSelection',
                        extend: ['BaseField'],
                        prototype: {
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

    ERPBlok.declare_react_class('FieldPassword', 'Password')
    AnyBlokJS.register({classname: 'FieldPassword',
                        extend: ['FieldString'],
                        prototype: {
        input_type: 'password',
        render_ro: function () {
            return <span>******</span>
        },
    }});

    ERPBlok.declare_react_class('FieldInteger', 'Integer')
    AnyBlokJS.register({classname: 'FieldInteger',
                        extend: ['FieldString'],
                        prototype: {
        input_type: 'number',
        get_step: function () {
            return '1';
        },
        render_rw: function () {
            var step = this.get_step();
            return <input type={this.input_type}
                          required={this.is_not_nullable()}
                          value={this.state.value}
                          style={this.get_style()}
                          step={step}
                          onKeyPress={this.onKeyPress.bind(this)}
                          onChange={this.handleChange.bind(this)}
                    />
        },
    }});

    ERPBlok.declare_react_class('FieldFloat', 'Float')
    AnyBlokJS.register({classname: 'FieldFloat',
                        extend: ['FieldInteger'],
                        prototype: {
        get_step: function () {
            return this.props.options.precision || '0.01';
        },
    }});

    ERPBlok.declare_react_class('FieldLargeBinary', 'LargeBinary')
    AnyBlokJS.register({classname: 'FieldLargeBinary',
                        extend: ['FieldString'],
                        prototype: {
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
            var placeholder = this.props.options.placeholder || '',
                accept = this.props.options.accept || "*";
            return <input type={this.input_type}
                          required={this.is_not_nullable()}
                          placeholder={placeholder}
                          value={this.state.value}
                          style={this.get_style()}
                          onKeyPress={this.onKeyPress.bind(this)}
                          onChange={this.handleChange.bind(this)}
                          accept={accept}
                    />
        },
    }});

    ERPBlok.declare_react_class('FieldPicture', 'Picture')
    AnyBlokJS.register({classname: 'FieldPicture',
                        extend: ['FieldLargeBinary'],
                        prototype: {
        render_ro: function () {
            var txt = this.get_title();
            return <img title={txt} src={this.state.value}/>
        },
    }});

    ERPBlok.declare_react_class('FieldBoolean', 'Boolean')
    AnyBlokJS.register({classname: 'FieldBoolean',
                        extend: ['BaseField'],
                        prototype: {
        handleChange: function (event) {
            this.props.update_field(this.props.options.id, event.target.checked);
        },
        render: function () {
            if (!this.is_visible()) return <div/>
            return (<input type="checkbox"
                           disabled={this.is_readonly()}
                           id={this.props.options.id}
                           onChange={this.handleChange.bind(this)}
                           checked={this.state.value} />)
        },
    }});

    ERPBlok.declare_react_class('FieldMany2One', 'Many2One');
    ERPBlok.add_field_definition('One2One', 'FieldMany2One');
    AnyBlokJS.register({classname: 'FieldMany2One',
                        extend: ['BaseField', 'RPC'],
                        prototype: {
        rpc_url: '/web/client/field',
        getInitialState: function () {
            var state = this._super();
            state.label = '';
            return state;
        },
        setState: function (states) {
            if ('value' in states) {
                if (states.value) {
                    if (JSON.stringify(this.state.value) != JSON.stringify(states.value)) {
                        var self = this;
                        this.rpc('x2One_render', {model: this.props.options.model,
                                                  primary_keys: states.value}, function (label) {
                            self.setState({'label': label})
                        });
                    }
                }
            }
            this._super(states)
        },
        onClick: function (event) {
            if (this.state.value) {
                var self = this;
                this.rpc('get_action_for', {model: this.props.options.model,
                                            view_type: 'Model.UI.View.Form',
                                            label: this.props.options.label}, function (action_description) {
                    var action = AnyBlokJS.new('Action', self.props.options.actionManager);
                    action.load(action_description, action_description.selected,
                                JSON.stringify(self.state.value));
                });
            }
        },
        handleChange: function (event) {
            this.setState({label: event.target.value});
            this.props.update_field(this.props.options.id, null);
        },
        search_more: function () {
            console.log('Search more');
        },
        add_new_entry: function () {
            if (this.state.value) {
                var self = this;
                this.rpc('get_action_for', {model: this.props.options.model,
                                            view_type: 'Model.UI.View.Form',
                                            label: this.props.options.label}, function (action_description) {
                    var action = AnyBlokJS.new('Action', self.props.options.actionManager);
                    action.callback_compute_pks = function (pks) {
                        self.props.update_field(self.props.options.id, pks);
                    }
                    action.load(action_description, action_description.selected, 'new');
                });
            }
        },
        componentDidUpdate: function() {
            if (this.is_readonly()) return
            var self = this,
                limit = this.props.options['search-box-limit'] || 15,
                add = this.props.options['search-box-add'] || true;  // FIXME use access rule
            this.input_el = $( "input#" + this.get_id() )
            this.input_el.autocomplete({
                source: function(request, response) {
                    self.rpc('x2One_search', {model: self.props.options.model,
                                              value: request.term}, function (values) {
                        var choices = $.map(values, function (value) {
                            return {label: value[1], 'value': value[1], pks: value[0]};
                        });
                        if (limit != -1 && choices.length > limit) {
                            choices = choices.slice(0, limit);
                            choices.push({
                                label: 'Search more ...',
                                fnct: self.search_more.bind(self),
                            });
                        }
                        if (add) {
                            choices.push({
                                label: 'Add new entry',
                                fnct: self.add_new_entry.bind(self),
                            });
                        }
                        // we doesn't filter here
                        response(choices);
                    });
                },
                select: function( event, ui ) {
                    if (ui.item.pks) {
                        self.props.update_field(self.props.options.id, ui.item.pks);
                    } else if (ui.item.fnct) {
                        ui.item.fnct();
                    }
                    return false;
                },
                autoFocus: true,
                delay: 250,
            });
        },
        get_id: function () {
            if (!this.field_id) this.field_id = 'x2O-id-for-' + this.props.options.id + '-' + get_field_counter();
            return this.field_id;
        },
        onBlur: function (event) {
            if (! this.state.value && this.state.label) {
                this.setState({label: ''});
            }
        },
        render_ro: function() {
            return <a onClick={this.onClick.bind(this)}>{this.state.label}</a>
        },
        render_rw: function () {
            var placeholder = this.props.options.placeholder || '',
                link = [];

            if (this.state.value) {
                link = <div className="input-group-button">
                           <a className="button"
                              onClick={this.onClick.bind(this)}>
                               <i className="fi-page-export" />
                           </a>
                       </div>
            }
            return (<div className="ui-widget input-group">
                        <input type="text"
                               id={this.get_id()}
                               className="input-group-field"
                               required={this.is_not_nullable()}
                               value={this.state.label}
                               style={this.get_style()}
                               onBlur={this.onBlur.bind(this)}
                               onKeyPress={this.onKeyPress.bind(this)}
                               onChange={this.handleChange.bind(this)}
                        />
                        {link}
                    </div>)
        },
    }});

    ERPBlok.declare_react_class('FieldMany2ManyChoices', 'Many2ManyChoices');
    AnyBlokJS.register({classname: 'FieldMany2ManyChoices',
                        extend: ['BaseField', 'RPC'],
                        prototype: {
        rpc_url: '/web/client/field',
        getInitialState: function () {
            var state = this._super();
            state.choices = [];
            return state;
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
            if (!this.is_visible()) return <div/>
            var choices = [],
                self = this,
                disabled = (this.is_readonly()) ? true : false,
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
            return (<fieldset className="fieldset"
                              style={this.get_style()}>
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

    ERPBlok.declare_react_class('FieldText', 'Text')
    AnyBlokJS.register({classname: 'FieldText',
                        extend: ['BaseField'],
                        prototype: {
        handleChange: function (event) {
            var $el = $('#' + this.get_id()),
                value = $el.val();
            this.props.update_field(this.props.options.id, value);
        },
        get_style: function () {
            var style = this._super();
            style.resize = 'none';
            return style;
        },
        get_id: function () {
            if (!this.field_id) this.field_id = 'Text-id-for-' + this.props.options.id + '-' + get_field_counter();
            return this.field_id;
        },
        componentDidUpdate: function() {
            var $el = $('#' + this.get_id());
            if ($el.length) {
                $el.val(this.state.value);
            }
        },
        render_rw: function () {
            var placeholder = this.props.options.placeholder || '',
                rows = this.props.options.rows || 10;
            return (<textarea id={this.get_id()}
                              placeholder={placeholder}
                              style={this.get_style()}
                              rows={rows}
                              disabled={false}
                              onChange={this.handleChange.bind(this)} />)
        },
    }});

    ERPBlok.declare_react_class('FieldHtml', 'Html')
    AnyBlokJS.register({classname: 'FieldHtml',
                        extend: ['BaseField'],
                        prototype: {
        get_id: function () {
            if (!this.field_id) this.field_id = 'Html-id-for-' + this.props.options.id + '-' + get_field_counter();
            return this.field_id;
        },
        componentDidUpdate: function() {
            if (!this.eltrumbowyg) {
                this.eltrumbowyg = $('#' + this.get_id())
                this.eltrumbowyg.trumbowyg({
                    fullscreenable: false,
                })
                .on('tbwblur', this.handleBlur.bind(this));
            }
            this.eltrumbowyg.trumbowyg('html', this.state.value);
        },
        componentWillUnmount: function() {
            if (!this.eltrumbowyg.length) this.eltrumbowyg.trumbowyg('destroy');
        },
        handleBlur: function (event) {
            if (this.eltrumbowyg.length) {
                this.props.update_field(this.props.options.id,
                                        this.eltrumbowyg.trumbowyg('html'));
            }
        },
        render_ro: function () {
            return (<span className="field-html"
                          dangerouslySetInnerHTML={{__html: this.state.value}} />)
        },
        render_rw: function () {
            var placeholder = this.props.options.placeholder || '';
            return (<div id={this.get_id()}
                         placeholder={placeholder}
                         style={this.get_style()} />)
        },
    }});
}) ();
