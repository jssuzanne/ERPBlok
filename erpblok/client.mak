<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1.0, user-scalable=no"/>
        <title>${title}</title>
        % for x in css:
            <link rel="stylesheet" type="text/css" href="${x}" ></link>
        % endfor
    </head>
    <body>
        <div class="top-bar">
            <div id="topbarleft" class="top-bar-left">
            </div>
            <div id="topbarright" class="top-bar-right">
            </div>
        </div>
        <div id="app">
        </div>
        <div class="reveal large" id="revealtopbarleft" data-reveal>
        </div>
        <div class="reveal large" id="revealtopbarright" data-reveal>
        </div>
        <div class="reveal large" id="errormanager" data-reveal>
            <button class="close-button" data-close aria-label="Close reveal" type="button">
                <span aria-hidden="true"></span>
            </button>
            <div></div>
        </div>
        <div id="erpblok-loader"></div>
        % for x in js:
            <script type="text/javascript" src="${x}" ></script>
        % endfor
        % for x in js_babel:
            <script type="text/babel" src="${x}" ></script>
        % endfor
        <script type="text/javascript">
            var $body = $("body"),
                loader_activity = false;

            $(document).on({
                ajaxStart: function() {
                    loader_activity = true;
                    setTimeout(function(){
                        if (loader_activity)
                            $body.addClass("loading");
                    }, 1000);
                },
                ajaxStop: function() {
                    loader_activity = false;
                    $body.removeClass("loading");
                },
            });
        </script>
        <script type="text/babel">
            ERPBlok.compile_react_classes();
            document.ERPBlokClient = AnyBlokJS.new('Client');
            document.ERPBlokClient.load();
        </script>
        ${templates | n}
    </body>
</html>
