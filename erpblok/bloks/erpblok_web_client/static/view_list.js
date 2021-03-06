(function () {
    AnyBlokJS.register({
        classname: 'View.List',
        extend: ['View.MultiEntries'],
        prototype: {
            title_selector: 'List view',
            icon_selector: 'fi-list',
            class_name: 'view-list',
            template: 'ViewList',
            getViewEl: function($action) {
                var self = this;
                var $el = this._super($action);
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
            get_entry: function (record, readonly=true) {
                return AnyBlokJS.new('View.List.Line', this, record, readonly);
            },
            render_records: function (records) {
                this._super(records);
                var self = this;
                if (this.options.inline) {
                    var colspan = this.options.fields2display.length + 1;
                    if (this.options.checkbox) rowspaw ++;
                    this.$nodeAdd = $('<tr><td colspan=' + colspan + '><a><i class="fi-page-add" />Add new line</a></td></tr>')
                    this.$nodeAdd.appendTo(this.$el.find('tbody'));
                    this.$nodeAdd.find('a').click(function (event) {
                        self.add_new_line();
                    });
                }
            },
            add_new_line: function () {
                var self = this;
                $.each(this.entries, function (i, line) {
                    line.closeLineWithoutSave();
                });
                this.rpc('new_entry', {model: this.viewManager.action.value.model,
                                       fields: this.options.fields}, function (record) {
                    var line = self.render_record(record, false);
                    line.id = {}; // force to have no id because it a new
                    line.$el.insertBefore(self.$nodeAdd);
                    $(line.$el.find('field input')[0]).focus();
                });
            },
            hide_show_buttons: function() {
                var checked = this.$el.find('input#line_checkbox:checked').length;
                this.viewManager.topButtons.setState({selected: checked});
            },
        },
    });
    AnyBlokJS.register({
        classname: 'View.List.Line',
        extend: ['View.Entry'],
        prototype: {
            template: 'ViewListLine',
            init: function(view, record, readonly=true) {
                this._super(view, record, readonly);
                this.selected = false;
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
                        <InlineCrudButtons readonly={this.readonly} line={this}/>,
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
                var isArray = false;
                if (Array.isArray(value) || Array.isArray(this.record[field_name]))
                    isArray = true;

                if (isArray || (value != this.record[field_name])) {
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
                        all_fields_value: self.record,
                        readonly: self.isReadonly(field.id)});
                });
                this.inline_buttons.setState({readonly: this.readonly});
                this.updateVisibilityUI();
            },
            pressEnter: function () {
                var self = this;
                this.rpc('set_entry', {model: self.view.viewManager.action.value.model,
                                       primary_keys: self.id,
                                       values: self.changed_record,
                                       fields: this.view.options.fields}, function (record) {
                    self.updateLine(record);
                    self.view.add_new_line();
                });
            },
            openLine: function() {
                this.readonly = false;
                this.applyChange();
            },
            closeLineWithoutSave: function() {
                this.readonly = true;
                this.changed_record = {};
                this.applyChange();
                if (Object.getOwnPropertyNames(this.id).length == 0) {
                    // No id == no record in the database
                    this.view.remove_entry(this);
                }
            },
            updateLine: function(record) {
                this.readonly = true;
                this.record = record;
                this.changed_record = {};
                this.applyChange();
                if (Object.getOwnPropertyNames(this.id).length == 0) {
                    this.compute_id();
                }
            },
            closeLineWithSave: function() {
                var self = this,
                    values = this.changed_record;
                if (this.view.viewManager.action.callback_save_changed_record) {
                    this.rpc('dummy_set_entry', {model: this.view.viewManager.action.value.model,
                                                 values: values,
                                                 fields: this.view.options.fields}, function (record) {
                        self.updateLine(record);
                        self.viewManager.action.callback_save_changed_record(record);
                    });
                } else {
                    this.rpc('set_entry', {model: self.view.viewManager.action.value.model,
                                           primary_keys: self.id,
                                           values: values,
                                           fields: this.view.options.fields}, function (record) {
                        self.updateLine(record);
                    });
                }
            },
            removeLine: function() {
                var self = this;
                this.rpc('del_entries', {model: self.view.viewManager.action.value.model,
                                         primary_keys: [self.id]}, function (removed) {
                    if (removed) self.view.remove_entry(self);
                });
            },
        },
    });
    ERPBlok.declare_react_class('InlineCrudButtons')
    AnyBlokJS.register({classname: 'InlineCrudButtons', prototype: {
        getInitialState: function () {
            return {readonly: this.props.readonly};
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
    AnyBlokJS.register({classname: 'InlineCrudButton', prototype: {
        icon: undefined,
        title: '',
        render:  function () {
            return (<li title={this.title}>
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
        title: 'Modify the line',
        onClick: function (event) {
            this.props.line.openLine();
        },
    }});
    ERPBlok.declare_react_class('InlineCrudButtonSave')
    AnyBlokJS.register({classname: 'InlineCrudButtonSave',
                        extend: ['InlineCrudButton'],
                        prototype: {
        icon: 'fi-save',
        title: 'Save the line',
        onClick: function (event) {
            this.props.line.closeLineWithSave();
        },
    }});
    ERPBlok.declare_react_class('InlineCrudButtonCancel')
    AnyBlokJS.register({classname: 'InlineCrudButtonCancel',
                        extend: ['InlineCrudButton'],
                        prototype: {
        icon: 'fi-x-circle',
        title: 'Cancel the modification',
        onClick: function (event) {
            this.props.line.closeLineWithoutSave();
        },
    }});
    ERPBlok.declare_react_class('InlineCrudButtonRemove')
    AnyBlokJS.register({classname: 'InlineCrudButtonRemove',
                        extend: ['InlineCrudButton'],
                        prototype: {
        icon: 'fi-trash',
        title: 'Remove the line',
        onClick: function (event) {
            this.props.line.removeLine();
        },
    }});
}) ();
