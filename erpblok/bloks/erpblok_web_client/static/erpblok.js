(function () {
    AnyBlokJS.register({
        classname: 'ERPBlok',
        prototype: {
            load: function () {
                this.offCanvasLeft = new Foundation.OffCanvas($('#offCanvasLeft.off-canvas'));
                this.offCanvasRight = new Foundation.OffCanvas($('#offCanvasRight.off-canvas'));
                this.dropdownTopBarLarge = new Foundation.DropdownMenu($('#topbar-menu-large'));
                this.accordionMenuLarge = new Foundation.AccordionMenu($('#accordion-menu-large'));
                this.accordionMenuSmall = new Foundation.AccordionMenu($('#accordion-menu-small'));
                this.hashTagManager = AnyBlokJS.new('HashTagManager', this);
                this.menuManager = AnyBlokJS.new('MenuManager', this);
                this.actionManager = AnyBlokJS.new('ActionManager', this);

                // Apply current hashTag
                this.hashTagManager.changed(this.hashTagManager.toObject(window.location.hash), {});
            },
        },
    });
}) ();
