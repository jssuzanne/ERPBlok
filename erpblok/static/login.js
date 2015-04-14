$(document).ready(function(){
    // Save the main hash in case of we want keep it for open action and view and other
    var hash = window.location.hash;
    $("#submit").click(function (){
        var $error = $("#error")
        $error.addClass("hide");
        var database = $("#database").val();
        var login = $("#login").val();
        var password = $("#password").val();
        if (database && login && password) {
            $.ajax({
                type: "POST",
                url:"/login/connect",
                data: {database: database, login: login, password: password}})
            .fail(function (xhr, status) {
                $error.removeClass("hide");
                $error.children().remove()
                if (xhr.status == 401) {
                    $error.append('<div>Wrong Login or Password</div>');
                } else {
                    $error.append('<div>Unknown error</div>');
                }
            })
            .done(function (url) {
                window.location = url + hash;
            });
        }
    });
});
