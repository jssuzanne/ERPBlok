(function () {
    ERPBlok.declare_react_class('SideMenu')
    AnyBlokJS.register({classname: 'SideMenu', prototype: {
        render: function () {
            var menus = [],
                self = this;
            this.props.menus.forEach(function (menu) {
                if (menu.children.length == 0) {
                    menus.push(<MenuLeaf space={self.props.space} options={menu}/>)
                } else {
                    menus.push(<MenuNode space={self.props.space} options={menu}/>)
                }
            });
            return (<ul className="vertical menu" data-accordion-menu>
                        {menus}
                    </ul>)
        },
    }});
    ERPBlok.declare_react_class('TopMenu')
    AnyBlokJS.register({classname: 'TopMenu', prototype: {
        render: function () {
            var menus = [],
                self = this;
            this.props.menus.forEach(function (menu) {
                if (menu.children.length == 0) {
                    menus.push(<MenuLeaf space={self.props.space} options={menu}/>)
                } else {
                    menus.push(<MenuNode space={self.props.space} options={menu}/>)
                }
            });
            return (<ul className="menu" >
                        {menus}
                    </ul>)
        },
    }});
    ERPBlok.declare_react_class('MenuLeaf')
    AnyBlokJS.register({classname: 'MenuLeaf', prototype: {
        render: function () {
            var id = this.props.options.id,
                action = this.props.options.action,
                space = this.props.space,
                href = '#clean-breadcrumbs=true&space=' + space + '&menu=' + id + '&action=' + action,
                clsmenu = 'menu-' + this.props.options.id;
            return (<li>
                        <a href={href} className={clsmenu}>
                            <h6>{this.props.options.label}</h6>
                        </a>
                    </li>)
        },
    }});
    ERPBlok.declare_react_class('MenuNode')
    AnyBlokJS.register({classname: 'MenuNode', prototype: {
        render: function () {
            var id = this.props.options.id,
                children = [],
                self = this,
                menuid = 'menu_' + this.props.options.id,
                clsmenu = "menu vertical nested menu-" + id;
            this.props.options.children.forEach(function (menu) {
                if (menu.children.length == 0) {
                    children.push(<MenuLeaf space={self.props.space} options={menu}/>)
                } else {
                    children.push(<MenuNode space={self.props.space} options={menu}/>)
                }
            });
            return (<li id={menuid}>
                        <a href="#"><h5>{this.props.options.label}</h5></a>
                        <ul className={clsmenu}>
                            {children}
                        </ul>
                    </li>)
        },
    }});
}) ();
