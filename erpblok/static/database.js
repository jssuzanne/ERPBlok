$(document).ready(function(){
    var elem = new Foundation.OffCanvas($('.off-canvas'));
    var $create = $('li#create a');
    var $drop = $('li#drop a');
    var $error = $('#error');
    var $error2 = $('#error2');
    var $error3 = $('#error3');
    var $blok_manager = $("div#create #db_manager_blok_manager");
    var $demo = $("div#create #db_manager_demo");

    function hide_error() {
        $error.addClass("hide");
        $error2.addClass("hide");
        $error3.addClass("hide");
    }

    function default_value($el) {
        if ($el.attr('default-value') == "True") {
            $el[0].checked = true;
        } else {
            $el[0].checked = false;
        }
    }

    default_value($blok_manager);
    default_value($demo);
    function goto_create () {
        default_value($blok_manager);
        default_value($demo);
        hide_error();
        $("#db_manager_password").val("");
        $("div#create").removeClass('hide');
        $("div#drop").addClass('hide');
        $drop.removeClass('is-active');
        $create.addClass('is-active');
        $("div#create #database").val("");
        $("div#create #login").val("admin");
        $("div#create #password").val("");
        $("div#create #password2").val("");
    }
    $create.click(function (event) {
        goto_create();
        elem.close();
    });
    $drop.click(function (event) {
        $("#db_manager_password").val("");
        $("div#create").addClass('hide');
        $("div#drop").removeClass('hide');
        $drop.addClass('is-active');
        $create.removeClass('is-active');
        hide_error();
        $.ajax({
            type: "POST",
            url:"/database/manager/list",
            data: {}})
        .done(function (html) {
            var $select = $("div#drop #select");
            $select.children().remove();
            $select.append(html);
            elem.close();
        });
    });
    $("#submit-create").click(function (){
        hide_error();
        var database = $("div#create #database").val();
        var login = $("div#create #login").val();
        var password = $("div#create #password").val();
        var password2 = $("div#create #password2").val();
        var db_manager_password = $("#db_manager_password").val();
        var blok_manager = $blok_manager[0].checked;
        var demo = $demo[0].checked;
        if (password != password2) {
            $error2.removeClass('hide');
        } else if (database && login && password) {
            $.ajax({
                type: "POST",
                url:"/database/manager/create",
                data: {database: database, login: login, password: password,
                       blok_manager:blok_manager, demo:demo,
                       db_manager_password:db_manager_password}})
            .fail(function (xhr, status) {
                if (xhr.status == 401) {
                    $error3.removeClass("hide");
                }
                if (xhr.status == 403) {
                    $error.removeClass("hide");
                }
            })
            .done(function (url) {
                window.location = url;
            });
        }
    });
    $("#submit-drop").click(function (){
        hide_error();
        var database = $("div#drop #select select").val();
        var db_manager_password = $("#db_manager_password").val();
        if (database) {
            $.ajax({
                type: "POST",
                url:"/database/manager/drop",
                data: {database: database, db_manager_password:db_manager_password}})
            .fail(function (xhr, status) {
                if (xhr.status == 401) {
                    $error3.removeClass("hide");
                }
            }).done (function () {
                goto_create();
            });
        }
    });
});
