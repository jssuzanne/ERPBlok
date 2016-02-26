(function () {

    ERPBlok.declare_react_class('Field')
    AnyBlokJS.register({classname: 'Field', prototype: {
        render_field_fake: function () {
            return this.render_field_String();
        },
        render_field_String: function () {
            return <FieldString options={this.props.options}
                                init_field={this.props.init_field}
                                is_readonly={this.props.is_readonly}
                                update_field={this.props.update_field} />
        },
        render_field_Boolean: function () {
            return <FieldBoolean options={this.props.options}
                                 init_field={this.props.init_field}
                                 is_readonly={this.props.is_readonly}
                                 update_field={this.props.update_field} />
        },
        render_field_Selection: function () {
            return <FieldSelection options={this.props.options}
                                   init_field={this.props.init_field}
                                   is_readonly={this.props.is_readonly}
                                   update_field={this.props.update_field} />
        },
        render_field_Password: function () {
            return <FieldPassword options={this.props.options}
                                init_field={this.props.init_field}
                                is_readonly={this.props.is_readonly}
                                update_field={this.props.update_field} />
        },
        render: function () {
            var fnct_name = 'render_field_' + (this.props.options.type || 'fake');
            if (this[fnct_name]) {
                return this[fnct_name]();
            } else {
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
        render_rw: function () {
            var required = this.props.options.nullable ? false : true,
                placeholder = this.props.options.placeholder || '';
            return <input type={this.input_type}
                          required={required}
                          placeholder={placeholder}
                          value={this.state.value}
                          style={this.get_style()}
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
        render_rw: function () {
            var options = [];
            this.props.options.selections.forEach(function (selection) {
                options.push(<option value={selection[0]}>{selection[1]}</option>)
            });
            // add css class for nullable
            return (<select value={this.state.value} 
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
                          className="switch-input"
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
}) ();
