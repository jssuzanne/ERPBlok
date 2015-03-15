$(document).ready(function(){
    function select_menu(menu) {
        $("li a.selected").removeClass('selected');
        $(menu).addClass('selected');
    }
    function goto_create () {
        $("div#create").removeClass('invisible');
        $("div#drop").addClass('invisible');
        select_menu("nav li a#create");
        $("div#create #database").val("");
        $("div#create #login").val("");
        $("div#create #password").val("");
    }
    $("nav #create").click(function(){
        goto_create();
    });
    $("nav #drop").click(function(){
        $("div#create").addClass('invisible');
        $("div#drop").removeClass('invisible');
        select_menu("nav li a#drop");
        $.ajax({
            type: "POST",
            url:"/database/manager/list",
            data: {}})
        .done(function (html) {
            var $select = $("div#drop #select");
            $select.children().remove();
            $select.append(html);
        });
    });
    $("#submit-create").click(function (){
        $("div#create #error").addClass("invisible");
        var database = $("div#create #database").val();
        var login = $("div#create #login").val();
        var password = $("div#create #password").val();
        if (database && login && password) {
            $.ajax({
                type: "POST",
                url:"/database/manager/create",
                data: {database: database, login: login, password: password}})
            .fail(function (xhr, status) {
                if (xhr.status == 403) {
                    $("div#create #error").removeClass("invisible");
                }
            })
            .done(function (url) {
                window.location = url;
            });
        }
    });
    $("#submit-drop").click(function (){
        var database = $("div#drop #select select").val();
        goto_create();
        if (database) {
            $.ajax({
                type: "POST",
                url:"/database/manager/drop",
                data: {database: database}});
        }
    });
});
