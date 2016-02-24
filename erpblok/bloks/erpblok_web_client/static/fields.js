(function () {

    ERPBlok.declare_react_class('Field')
    AnyBlokJS.register({classname: 'Field', prototype: {
        render_field_fake: function () {
            return this.render_field_string();
        },
        render_field_string: function () {
            return <FieldString options={this.props.options}
                                init_field={this.props.init_field}
                                is_readonly={this.props.is_readonly}
                                update_field={this.props.update_field} />
        },
        render_field_password: function () {
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

    ERPBlok.declare_react_class('FieldPassword')
    AnyBlokJS.register({classname: 'FieldPassword', extend: ['FieldString'], prototype: {
        input_type: 'password',
        render_ro: function () {
            return <span>******</span>
        },
    }});
}) ();
