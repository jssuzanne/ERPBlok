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
        <div id="ERPBLOKMAINAPP"></div>
        % for x in js:
            <script type="text/javascript" src="${x}" ></script>
        % endfor
        % for x in js_babel:
            <script type="text/babel" src="${x}" ></script>
        % endfor
        <script type="text/babel">
            ERPBlok.compile_react_classes();
            ReactDOM.render(<Client />, document.getElementById('ERPBLOKMAINAPP'));  
        </script>
        ${templates | n}
    </body>
</html>
