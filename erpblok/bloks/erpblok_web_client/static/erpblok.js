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
