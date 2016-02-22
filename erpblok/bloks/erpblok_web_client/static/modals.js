(function () {
    ERPBlok.declare_react_class('MenuRevealButton')
    AnyBlokJS.register({classname: 'MenuRevealButton', prototype: {
        getInitialState: function () {
            return this.props.getter();
        },
        render: function () {
            return (<ul class="menu">
                        <li>
                            <a onClick={this.props.click} >
                                <i className={this.state.icon} />
                                {this.state.label}
                            </a>
                        </li>
                    </ul>)
        },
    }});
    ERPBlok.declare_react_class('MenuRevealModal')
    AnyBlokJS.register({classname: 'MenuRevealModal', prototype: {
        getInitialState: function () {
            return {'menus': [], filterText: ''};
        },
        handleChange: function (event) {
            this.setState({filterText: event.target.value})
        },
        render: function () {
            var panels = [],
                self = this,
                filterText = this.state.filterText;
            this.state.menus.forEach(function(menu) {
                if (filterText) {
                    if (menu.label.indexOf(filterText) === -1) {
                        return;
                    }
                }
                var onClick = function () {
                    self.props.select(menu);
                }
                panels.push(<div className="column">
                                <div className="callout primary radius" 
                                     style={{cursor: 'pointer'}}
                                     onClick={onClick}>
                                    <div className="row">
                                        <div className="column small-2 medium-2 large-2">
                                             <i className={menu.icon} />
                                        </div>
                                        <div className="column small-10 medium-10 large-10">
                                            {menu.label}
                                        </div>
                                    </div>
                                </div>
                            </div>)
            });
            return (<div>
                        <div className="top-bar">
                            <div id="topbarright" className="top-bar-right"> 
                                <ul className="menu">
                                    <li>
                                        <input type="search" 
                                               className="radius"
                                               placeholder="Filter ..." 
                                               value={this.state.filterText}
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
                        </div>
                        <div style={{'overflow-y': 'scroll'}}>
                            <div className="row small-up-1 medium-up-2 large-up-4">
                                {panels}
                            </div>
                        </div>
                    </div>)
        },
    }});
}) ();
