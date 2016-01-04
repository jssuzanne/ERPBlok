$(document).ready(function(){
    var offCanvasLeft = new Foundation.OffCanvas($('#offCanvasLeft.off-canvas'));
    var offCanvasRight = new Foundation.OffCanvas($('#offCanvasRight.off-canvas'));
    var dropdownTopBarLarge = new Foundation.DropdownMenu($('#topbar-menu-large'));
    var accordionMenuLarge = new Foundation.AccordionMenu($('#accordion-menu-large'));
    var accordionMenuSmall = new Foundation.AccordionMenu($('#accordion-menu-small'));
    ERPBlok.hashTagManager = new ERPBlok.HashTagManager();
    ERPBlok.menuManager = new ERPBlok.MenuManager();
    ERPBlok.actionManager = new ERPBlok.ActionManager();

    // Apply current hashTag
    ERPBlok.hashTagManager.changed(ERPBlok.hashTagManager.toObject(window.location.hash), {});
});
