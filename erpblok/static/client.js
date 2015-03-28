$(document).ready(function(){
    $(document).foundation();
    ERPBlok.hashTagManager = new ERPBlok.HashTagManager();
    ERPBlok.menuManager = new ERPBlok.MenuManager();
    ERPBlok.actionManager = new ERPBlok.ActionManager();

    // Apply current hashTag
    ERPBlok.hashTagManager.changed(ERPBlok.hashTagManager.toObject(window.location.hash), {});
});
