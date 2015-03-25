$(document).ready(function(){
    $(".button-collapse").sideNav();
    $("header nav div.nav-wrapper .dropdown-button").dropdown({
        hover: false,
        constrain_width: true,
        alignment: 'right',
        belowOrigin: true,
    });

    ERPBlok.hashTagManager = new ERPBlok.HashTagManager();
    ERPBlok.menuManager = new ERPBlok.MenuManager();

    // Apply current hashTag
    ERPBlok.hashTagManager.changed(ERPBlok.hashTagManager.toObject(window.location.hash), {});
});
