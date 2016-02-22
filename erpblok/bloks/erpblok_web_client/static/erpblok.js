window.ERPBlok = null;
(function () {
    AnyBlokJS.register({classname: 'React', prototype: React.Component.prototype})

    var ERPBLOK = function () {this.init()};
    ERPBLOK.prototype = Object.create({
        init: function () {
            this.react_classes = [];
        },
        declare_react_class: function (classname) {
            if (this.react_classes.indexOf(classname) == -1) {
                this.react_classes.push(classname);
            }
        },
        compile_react_classes: function () {
            for (var index in this.react_classes) {
                var classname = this.react_classes[index];
                AnyBlokJS.register({classname: classname, extend: ['React']})
                window[classname] = AnyBlokJS.compile(classname);
                window[classname].prototype.constructor = function () {
                    if (this.init) {
                        this.init();
                    }
                    React.Component.prototype.constructor.apply(this, arguments);
                    var r = this.getInitialState ? this.getInitialState() : null;
                    this.state = r
                };
            }
        },
    });

    window.ERPBlok = new ERPBLOK()
}) ();

// var ERPBlok = new ERPBLOK();
/*
(function () {
    AnyBlokJS.register({
        classname: 'ERPBlok',
        prototype: {
            init: function () {
                this.init_foundation();
                this.init_object();
            },
            init_foundation: function () {
                this.offCanvasLeft = new Foundation.OffCanvas($('#offCanvasLeft.off-canvas'));
                this.offCanvasRight = new Foundation.OffCanvas($('#offCanvasRight.off-canvas'));
                this.dropdownTopBarLarge = new Foundation.DropdownMenu($('#topbar-menu-large'));
                this.accordionMenuLarge = new Foundation.AccordionMenu($('#accordion-menu-large'));
                this.accordionMenuSmall = new Foundation.AccordionMenu($('#accordion-menu-small'));
            },
            init_object: function () {
                var self = this;
                this.hashTagManager = AnyBlokJS.new('HashTagManager', this);
                this.menuManager = AnyBlokJS.new('MenuManager', this);
                this.actionManager = AnyBlokJS.new('ActionManager', this);
                $('.logout').click(function (event) {
                    self.logout ();
                });
                $('.toggle-menu').click(function (event) {
                    var mainmenu = $('#main-menu')
                    var mainapp = $('#main-app')
                    if (mainmenu.hasClass('hide')) {
                        mainmenu.removeClass('hide');
                        mainapp.addClass('large-9');
                    } else {
                        mainmenu.addClass('hide');
                        mainapp.removeClass('large-9');
                    }
                });
            },
            load: function () {
                this.hashTagManager.changed(this.hashTagManager.toObject(window.location.hash), {});
            },
            logout: function () {
                $.ajax({type: "POST",
                        url: "/login/disconnect",
                        data: {}})
                .done(function (url) {
                    window.location = url;
                });
            },
        },
    });
}) ();
*/
