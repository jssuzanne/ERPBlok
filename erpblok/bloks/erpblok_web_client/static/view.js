(function () {
    AnyBlokJS.register({
        classname: 'ViewManager',
        extend: ['Template'],
        prototype: {
            template: 'ViewManager',
            init: function(action, view_id, pks) {
                this.action = action;
                this.$action = action.$el;
                this.$el = this.render_template();
                this.$buttons = this.$el.find('div.view-buttons');
                this.topButtons = ReactDOM.render(
                    <ViewTopButtons view_id={view_id}
                                    call={this.callFunction.bind(this)}/>,
                    this.$buttons[0]);
                this.$el.appendTo(action.$el);
                this.views = {};
                this.active_view = undefined;
                for (var i in action.value.views) {
                    this.add(action.value.views[i]);
                }
                if (view_id == undefined) {
                    view_id = action.actionManager.get_hash('view');
                }
                if (view_id) {
                    var kwargs = {}
                    if (pks == undefined) {
                        pks = action.actionManager.get_hash('pks');
                    }
                    if (pks) {
                        kwargs.id = JSON.parse(pks);
                    }
                    this.select_view(view_id, kwargs);
                } else {
                    this.select_view(action.value.selected);
                }
            },
            callFunction: function(function_name, dataset) {
                this.views[this.active_view].view['on_' + function_name](dataset);
            },
            add: function(view) {
                var self = this;
                var view = this.get_view_cls(view);
                var $navEl = view.getNavEl();
                $navEl.click(function (event) {
                    self.select_view(event.currentTarget.id);
                });
                $navEl.appendTo(this.$el.find('ul'));
                var $viewEl = view.getViewEl();
                $viewEl.addClass('hide');
                $viewEl.appendTo(this.$action);
                this.views[view.options.id] = {
                    '$nav': $navEl,
                    '$view': $viewEl,
                    'view': view
                };
            },
            get_view_cls: function(view) {
                var viewName = 'View.' + view.mode;
                if (AnyBlokJS.class_names[viewName])
                    return AnyBlokJS.new(viewName, this, view);
                return AnyBlokJS.new('View', this, view);
            },
            select_view: function (view_id, kwargs) {
                if (view_id == this.active_view) return;
                if (this.active_view) {
                    this.views[this.active_view].$nav.removeClass('active');
                    this.views[this.active_view].$view.addClass('hide');
                }
                if (view_id && this.views[view_id]) {
                    this.views[view_id].$nav.addClass('active');
                    this.views[view_id].$view.removeClass('hide');
                    this.views[view_id].view.last_view = this.active_view || this.action.value.selected;
                    this.views[view_id].view.render(kwargs);
                    this.views[view_id].view.display_buttons();
                    this.action.actionManager.select_view(view_id, kwargs);
                    this.active_view = view_id;
                }
            },
        },
    });
    AnyBlokJS.register({
        classname: 'View',
        extend: ['RPC', 'Template'],
        template: 'View',
        prototype: {
            rpc_url: '/web/client/view',
            icon_selector: 'fi-alert',
            title_selector: 'undefined',
            class_name: 'view-undefined',
            template: 'View',
            init: function(viewManager, options) {
                this.viewManager = viewManager;
                this.options = options;
                this.readonly = true;
            },
            getNavEl: function(view_id) {
                return $($.templates('#ERPBlokViewSelector').render(
                    {'id': this.options.id,
                     'title_selector': this.title_selector,
                     'icon_selector': this.icon_selector,
                     'selectable': this.options.selectable}));
            },
            getViewEl: function() {
                this.$el = this.render_template({id: this.options.id, class_name: this.class_name});
                return this.$el;
            },
            render: function(args) {},
            transition: function(name, kwargs) {
                this['transition_' + name](kwargs);
            },
            transition_selectRecord: function(kwargs) {
                var selectRecord = [''];
                try {
                    selectRecord = this.options.transitions.selectRecord;
                } catch (err) {
                    console.warn(err);
                }
                if (selectRecord[0] == 'open_view') {
                    this.viewManager.select_view(selectRecord[1], kwargs);
                }
            },
            transition_newRecord: function(kwargs) {
                var newRecord = [''];
                try {
                    newRecord = this.options.transitions.newRecord;
                } catch (err) {
                    console.warn(err);
                }
                if (newRecord[0] == 'open_view') {
                    this.viewManager.select_view(newRecord[1], {id: null,
                                                                new: true});
                }
            },
            transition_closeView: function(kwargs) {
                if (this.last_view) {
                    this.viewManager.select_view(this.last_view, kwargs);
                }
            },
            get_field_cls: function(item) {
                var fieldName = 'Field.' + item.type;
                if (AnyBlokJS.class_names[fieldName])
                    return AnyBlokJS.new(fieldName, this, item);
                console.warn("Unknon type : " + item.type);
                return AnyBlokJS.new('Field', this, item);
            },
            toggleReadonly : function() {
                this.readonly = ! this.readonly;
                this.applyReadOnly();
            },
            applyReadOnly: function () {
                this.viewManager.topButtons.setState({readonly: this.readonly});
            },
            display_buttons: function() {
                this.viewManager.topButtons.setState({buttons: this.options.buttons || [],
                                                      groups: this.options.groups_buttons || []});
            },
            on_edit_view: function() {
                if (this.readonly) {
                    this.toggleReadonly();
                }
            },
            on_read_view: function() {
                if (! this.readonly) {
                    this.toggleReadonly();
                }
            },
            on_close_view: function () {
                if (! this.readonly) this.toggleReadonly();
                this.transition('closeView');
            },
            get_values_changed: function () {
            },
            rpc_call: function(pks, method, params, kwparams) {
                var self = this;
                this.rpc('call', {model: this.viewManager.action.value.model,
                                  primary_keys: pks,
                                  method: method,
                                  params: params || new Array(),
                                  kwparams: kwparams || {}}, function (result) {
                    self.parse_call_result(result);
                });
            },
            parse_call_result: function(result) {
                var self = this;
                $.each(result, function(name, value) {
                    if (name == 'action') {
                        self[value](result);
                    }
                });
            },
            reload: function(params) {
                this.viewManager.action.actionManager.reload(params.keephash || false);
            },
        },
    });
    ERPBlok.declare_react_class('ViewTopButtons')
    AnyBlokJS.register({classname: 'ViewTopButtons', prototype: {
        getInitialState: function () {
            var readonly = true;
            if (this.props.readonly != undefined) readonly = this.props.readonly;
            return {readonly: readonly,
                    selected: false,
                    buttons: this.props.buttons || [],
                    groups: this.props.groups || []};
        },
        is_visible: function (entity) {
            if (entity.visibility == "") return true;
            if (entity.visibility == 'on-readonly') {
                if (this.state.readonly) return true;
            }
            if (entity.visibility == 'on-readonly on-selected') {
                if (this.state.readonly && this.state.selected) return true;
            }
            if (entity.visibility == 'on-readwrite') {
                if (!this.state.readonly) return true;
            }
            return false;
        },
        get_buttons: function () {
            var buttons = [],
                self = this;
            this.state.buttons.forEach(function(button) {
                if (self.is_visible(button)) {
                    buttons.push(<ViewTopButton call={self.props.call} options={button} />);
                }
            });
            // FIXME
            // this.state.groups.forEach(function(group) {
            //     if (self.is_visible(group)) {
            //         buttons.push(<ViewTopGroup call={self.props.call}
            //                                    readonly={self.state.readonly}
            //                                    buttons={group.buttons}
            //                                    options={group} />);
            //     }
            // });
            return buttons;
        },
        render: function() {
            var buttons = this.get_buttons();
            return (<div className="button-group">
                        {buttons}
                    </div>)
        },
    }});
    ERPBlok.declare_react_class('ViewTopButton')
    AnyBlokJS.register({classname: 'ViewTopButton', prototype: {
        onClick: function (event) {
            this.props.call(this.props.options.fnct, this.props.options.method);
        },
        render: function() {
            return (<a className="view-button button"
                       onClick={this.onClick.bind(this)}>
                       {this.props.options.label}
                    </a>)
        },
    }});
    ERPBlok.declare_react_class('ViewTopGroup')
    AnyBlokJS.register({classname: 'ViewTopGroup',
                        extend: ['ViewTopButtons'],
                        prototype: {
        render: function() {
            var buttons = this.get_buttons();
            return (<a className="view-button dropdown button">
                       <span>{this.props.options.label}</span>
                        {buttons}
                    </a>)
        },
    }});
}) ();
