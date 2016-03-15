(function () {
    var breadcrumb_index = 0,
        getBreadCrumbIndex = function() {
            breadcrumb_index = breadcrumb_index + 1;
            return breadcrumb_index;
        }
    AnyBlokJS.register({
        classname: 'BreadCrumbManager',
        extend: ['Template'],
        prototype: {
            init: function(actionManager, $el) {
                this.links = [];
                this.actionManager = actionManager;
                this.el = ReactDOM.render(
                    <BreadCrumb on_click={this.on_click.bind(this)} />,
                    $el.find('div#breadcrumb')[0]);
            },
            add: function(action) {
                var index = getBreadCrumbIndex();
                if (this.links.length > 0) {
                    this.links[this.links.length - 1].action.$el.addClass('hide');
                }
                this.links.push({
                    index: index,
                    action: action,
                    hash: this.actionManager.client.hashTagManager.toObject(window.location.hash),
                });
                this.el.setState({links: this.links})
            },
            update_last_hashtag: function(hash) {
                this.links[this.links.length - 1].hash = $.extend(
                    {}, hash, this.links[this.links.length - 1].hash);
                this.actionManager.client.hashTagManager.update(hash);
            },
            on_click: function (index) {
                var links = [],
                    hash = undefined;
                for (var i in this.links) {
                    var link = this.links[i];
                    if (link.index <= index) {
                        links.push(link);
                        if (link.index == index) {
                            hash = link.hash;
                            link.action.$el.removeClass('hide');
                        }
                    } else {
                        link.action.$el.remove();
                    }
                }
                this.links = links;
                this.el.setState({links: links});
                this.actionManager.client.hashTagManager.update(hash, false);
            },
            clear_all: function () {
                for (var i in this.links) {
                    this.links[i].action.$el.remove();
                }
                this.links = [];
                this.el.setState({links: []});
            },
        },
    });
    ERPBlok.declare_react_class('BreadCrumb')
    AnyBlokJS.register({classname: 'BreadCrumb', prototype: {
        getInitialState: function () {
            return {links: []};
        },
        render: function () {
            var elements = [],
                self = this;
            this.state.links.forEach(function (link) {
                if (link.index == self.state.links[self.state.links.length - 1].index) {
                    elements.push(<li className="disabled">
                                      {link.action.value.label}
                                  </li>)
                } else {
                    var onClick = function (event) {
                        self.props.on_click(link.index);
                    }
                    elements.push(<li>
                                      <a onClick={onClick}>
                                          {link.action.value.label}
                                      </a>
                                  </li>)
                }
            });
            return (<ul className="breadcrumbs">
                        {elements}
                    </ul>)
        },
    }});
}) ();
