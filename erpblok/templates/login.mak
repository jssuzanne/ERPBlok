<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <link rel="stylesheet" type="text/css" href="/static/login.css">
        <script type="text/javascript" src="/static/jquery-2.1.3.min.js" ></script>
        <script type="text/javascript" src="/static/login.js" ></script>
        <title>${title}</title>
    </head>
    <body>
        <div id="global">
            <div class="panel">
                <img src="/login/logo" height="300" width="400"/>
                <div class="entry">
                    <label for="database">Database</label>
                    <select id="database" class="panel-input">
                    % for db in databases:
                        % if db == database:
                            <option value="${db}" selected>${db}</option> \
                        % else:
                            <option value="${db}">${db}</option> \
                        % endif
                    % endfor
                </select>
                </div>
                <div class="entry">
                    <label for="login">Login</label>
                    <input id="login" type="text" name="login" required class="panel-input"/>
                </div>
                <div class="entry">
                    <label for="password">Password</label>
                    <input id="password" type="text" name="password"
                           required class="panel-input"/>
                </div>
                <div id="error" class="invisible">
                </div>
                <input id="submit" type="button" value="Login" />
            </div>
            <a href="/database/manager">Database manager</a>
        </div>
    </body>
</html>
