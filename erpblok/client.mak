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
        <script type="text/babel">
            var $body = $("body"),
                loader_counter = 0;
            $(document).on({
                ajaxStart: function() {
                    loader_counter += 1;
                    setTimeout(function(){
                        if (loader_counter)
                            $body.addClass("loading");
                    }, 3000);
                },
                ajaxStop: function() {
                    loader_counter -= 1;
                    if (!loader_counter) $body.removeClass("loading");
                },
            });
            ERPBlok.compile_react_classes();
            document.ERPBlokClient = AnyBlokJS.new('Client');
            document.ERPBlokClient.load();
        </script>
        ${templates | n}
    </body>
</html>
