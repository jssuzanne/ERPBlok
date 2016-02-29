(function () {
    ERPBlok.declare_react_class('Menu')
    AnyBlokJS.register({classname: 'Menu', prototype: {
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
    ERPBlok.declare_react_class('MenuLeaf')
    AnyBlokJS.register({classname: 'MenuLeaf', prototype: {
        render: function () {
            var id = this.props.options.id,
                action = this.props.options.action,
                space = this.props.space,
                href = '#space=' + space + '&menu=' + id + '&action=' + action,
                menuid = 'menu' + this.props.options.id;
            return (<li>
                        <a href={href} id={menuid}>
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
            console.log(this.props)
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
