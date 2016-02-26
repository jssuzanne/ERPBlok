(function () {
    ERPBlok.declare_react_class('MenuRevealButton')
    AnyBlokJS.register({classname: 'MenuRevealButton', prototype: {
        getInitialState: function () {
            if (this.props.getter) {
                return this.props.getter();
            }
            return {icon: '', label: ''};
        },
        render: function () {
            return (<ul className="menu">
                        <li className="menu-text">
                            <h3>
                                <a onClick={this.props.click} > 
                                    {this.props.label}
                                </a>
                            </h3>
                        </li>
                        <li className="menu-text">
                            <h2>
                                <span >
                                    <i className={this.state.icon} />
                                    {this.state.label}
                                </span>
                            </h2>
                        </li>
                    </ul>)
        },
    }});
    ERPBlok.declare_react_class('MenuRevealModal')
    AnyBlokJS.register({classname: 'MenuRevealModal', prototype: {
        getInitialState: function () {
            return {'menus': [], filterText: ''};
        },
        handleUserInput: function (filterText) {
            this.setState({filterText: filterText});
        },
        render: function () {
            return (<div>
                        <MenuRevealModalSearchBar filterText={this.state.filterText}
                                                  close={this.props.close}
                                                  onUserInput={this.handleUserInput.bind(this)} />
                        <MenuRevealModalTable menus={this.state.menus}
                                              select={this.props.select}
                                              filterText={this.state.filterText} />    
                    </div>)
        },
    }});
    ERPBlok.declare_react_class('MenuRevealModalSearchBar')
    AnyBlokJS.register({classname: 'MenuRevealModalSearchBar',
                        prototype: {
        handleChange: function (event) {
            this.props.onUserInput(event.target.value);
        },
        render: function () {
            return (<div className="row">
                        <div className="columns large-9 medium-6"></div>
                        <div className="columns large-3 medium-6">
                            <ul className="menu">
                                <li>
                                    <i className="fi-magnifying-glass" />
                                </li>
                                <li>
                                    <input type="search" 
                                           placeholder="Filter ..." 
                                           value={this.props.filterText}
                                           onChange={this.handleChange.bind(this)} />
                                </li>
                                <li>
                                    <button type="button" 
                                            onClick={this.props.close}
                                            className="button">
                                        Close
                                    </button>
                                </li>
                            </ul>
                        </div>
                    </div>)
        },
    }});
    ERPBlok.declare_react_class('MenuRevealModalTable')
    AnyBlokJS.register({classname: 'MenuRevealModalTable',
                        prototype: {
        render: function () {
            var categories = [],
                self = this,
                filterText = this.props.filterText;
            this.props.menus.forEach(function(categ) {
                var panels = [];
                for (var index in categ.menus) {
                    var menu = categ.menus[index];
                    if (filterText) {
                        if (menu.label.indexOf(filterText) !== -1) {
                            panels.push(menu);
                        }
                        if (menu.description && menu.description.indexOf(filterText) !== -1) {
                            panels.push(menu);
                        }
                    } else {
                        panels.push(menu);
                    }
                }
                if (panels.length) {
                    categories.push(<MenuRevealModalTableCategory menus={panels} 
                                                                  select={self.props.select}
                                                                  icon={categ.icon}
                                                                  label={categ.label}/>)
                }
            });
            return (<div>
                        {categories}
                    </div>)
        },
    }});
    ERPBlok.declare_react_class('MenuRevealModalTableCategory')
    AnyBlokJS.register({classname: 'MenuRevealModalTableCategory',
                        prototype: {
        render: function () {
            var panels = [],
                self = this;
            this.props.menus.forEach(function (menu) {
                panels.push(<MenuRevealModalTablePanel label={menu.label}
                                                       name={menu.id}
                                                       icon={menu.icon} 
                                                       description={menu.description}
                                                       select={self.props.select} />);
            });
            return (<fieldset className="fieldset">
                        <legend>
                            <h3>
                                <i className={this.props.icon} />
                                {this.props.label}
                            </h3>
                        </legend>
                        <div className="row small-up-1 medium-up-2 large-up-4">
                            {panels}
                        </div>
                    </fieldset>)
        },
    }});
    ERPBlok.declare_react_class('MenuRevealModalTablePanel')
    AnyBlokJS.register({classname: 'MenuRevealModalTablePanel',
                        prototype: {
        onClick: function () {
            this.props.select(this.props.name);
        },
        render: function () {
            return (<div className="column">
                        <div className="callout primary radius" 
                             onClick={this.onClick.bind(this)}
                             style={{cursor: 'pointer'}} >
                            <div className="row">
                                <div className="column small-2 medium-2 large-2">
                                    <i className={this.props.icon} />
                                </div>
                                <div className="column small-10 medium-10 large-10">
                                    <h5>{this.props.label}</h5>
                                </div>
                            </div>
                            <div className="row">
                                <span>
                                    {this.props.description}
                                </span>
                            </div>
                        </div>
                    </div>)
        },
    }});
}) ();
