(function () {
    AnyBlokJS.register({
        classname: 'View.List',
        extend: ['View.MultiEntries'],
        prototype: {
            title_selector: 'List view',
            icon_selector: 'fi-list',
            class_name: 'view-list',
            template: 'ViewList',
            getViewEl: function() {
                var self = this;
                var $el = this._super();
                $el.find('input#all_checkbox').click(function (event) {
                    var checked = $(event.currentTarget).prop('checked');
                    self.$el.find('input#line_checkbox').prop('checked', checked);
                    self.hide_show_buttons()
                });
                return $el;
            },
            appendToView: function(line) {
                line.$el.appendTo(this.$el.find('tbody'));
            },
            get_entry: function (record) {
                return AnyBlokJS.new('View.List.Line', this, record);
            },
            hide_show_buttons: function() {
                var checked = this.$el.find('input#line_checkbox:checked').length;
                this.viewManager.$buttons.find('.on-readonly').addClass('hide');
                this.viewManager.$buttons.find('.on-selected').addClass('hide');
                this.viewManager.$buttons.find('.on-readwrite').addClass('hide');
                if (this.readonly && checked) {
                    this.viewManager.$buttons.find('.on-readonly.on-selected, .on-readonly:not(.on-selected)').removeClass('hide');
                } else if (this.readonly) {
                    this.viewManager.$buttons.find('.on-readonly:not(.on-selected)').removeClass('hide');
                } else {
                    if (checked) {
                        this.viewManager.$buttons.find('.on-selected:not(.on-readonly)').removeClass('hide');
                        this.viewManager.$buttons.find('.on-readwrite').removeClass('hide');
                    } else {
                        this.viewManager.$buttons.find('.on-readwrite:not(.on-selected)').removeClass('hide');
                    }
                }
            },
        },
    });
    AnyBlokJS.register({
        classname: 'View.List.Line',
        extend: ['View.Entry'],
        prototype: {
            template: 'ViewListLine',
            init: function(view, record) {
                this._super(view, record);
                this.selected = false;
                this.changed_record = {};
            },
            render: function () {
                var self = this;
                this._super();
                this.$el.find('input#line_checkbox').click(function () {
                    var nb = self.view.$el.find('input#line_checkbox:not(:checked)').length;
                    if (nb) {
                        self.view.$el.find('input#all_checkbox').prop('checked', false);
                    } else {
                        self.view.$el.find('input#all_checkbox').prop('checked', true);
                    }
                    if (self.$el.find('input#line_checkbox:checked').length) {
                        self.selected = true;
                    } else {
                        self.selected = false;
                    }
                    self.view.hide_show_buttons()
                })
                if (this.view.options.inline) {
                    this.inline_buttons = ReactDOM.render(
                        <InlineCrudButtons line={this}/>,
                        this.$el.find('inline-crud-buttons')[0]);
                } else {
                    this.$el.find('td.selectable').click(function () {
                        if (self.view.readonly) {
                            self.view.transition('selectRecord', {id: self.id});
                        }
                    });
                }
            },
            updateField: function (field_id, value) {
                this._super(field_id, value);
                var field_name = this.view.get_field(field_id).field_name;
                if (value != this.record[field_name]) {
                    this.changed_record[field_name] = value;
                } else {
                    if (this.changed_record[field_name]) {
                        delete this.changed_record[field_name];
                    }
                }
            },
            applyChange: function () {
                var self = this;
                $.each(this.view.options.fields2display, function (i, field) {
                    self.fields_by_ids[field.id].setState({
                        value: self.record[field.field_name],
                        readonly: self.isReadonly(field.id)});
                });
                this.inline_buttons.setState({readonly: this.readonly});
            },
            openLine: function() {
                this.readonly = false;
                this.applyChange();
            },
            closeLineWithoutSave: function() {
                this.readonly = true;
                this.changed_record = {};
                this.applyChange();
            },
            closeLineWithSave: function() {
                this.readonly = true;
                // call rpc save line
                this.applyChange();
            },
            removeLine: function() {
                // call rpc remove line
            },
        },
    });
    ERPBlok.declare_react_class('InlineCrudButtons')
    AnyBlokJS.register({classname: 'InlineCrudButtons', prototype: {
        getInitialState: function () {
            return {readonly: true};
        },
        render: function () {
            var buttons = [];
            if (this.state.readonly) {
                buttons.push(<InlineCrudButtonOpen line={this.props.line}/>);
                buttons.push(<InlineCrudButtonRemove line={this.props.line}/>);
            } else {
                buttons.push(<InlineCrudButtonSave line={this.props.line}/>);
                buttons.push(<InlineCrudButtonCancel line={this.props.line}/>);
            }
            return (<nav className='view-list-inline-buttons'>
                        <ul>
                            {buttons}
                        </ul>
                    </nav>)
        },
    }});
    ERPBlok.declare_react_class('InlineCrudButton')
    AnyBlokJS.register({classname: 'InlineCrudButton', prototype: {
        icon: undefined,
        onClick: function (event) {},
        render:  function () {
            return (<li title="Modify the line">
                        <a onClick={this.onClick.bind(this)}>
                            <i className={this.icon} />
                        </a>
                    </li>)
        },
    }});
    ERPBlok.declare_react_class('InlineCrudButtonOpen')
    AnyBlokJS.register({classname: 'InlineCrudButtonOpen', 
                        extend: ['InlineCrudButton'],
                        prototype: {
        icon: 'fi-page-edit',
        onClick: function (event) {
            this.props.line.openLine();
        },
    }});
    ERPBlok.declare_react_class('InlineCrudButtonSave')
    AnyBlokJS.register({classname: 'InlineCrudButtonSave', 
                        extend: ['InlineCrudButton'],
                        prototype: {
        icon: 'fi-save',
        onClick: function (event) {
            this.props.line.closeLineWithSave();
        },
    }});
    ERPBlok.declare_react_class('InlineCrudButtonCancel')
    AnyBlokJS.register({classname: 'InlineCrudButtonCancel', 
                        extend: ['InlineCrudButton'],
                        prototype: {
        icon: 'fi-x-circle',
        onClick: function (event) {
            this.props.line.closeLineWithoutSave();
        },
    }});
    ERPBlok.declare_react_class('InlineCrudButtonRemove')
    AnyBlokJS.register({classname: 'InlineCrudButtonRemove', 
                        extend: ['InlineCrudButton'],
                        prototype: {
        icon: 'fi-trash',
        onClick: function (event) {
            this.props.line.removeLine();
        },
    }});
}) ();
