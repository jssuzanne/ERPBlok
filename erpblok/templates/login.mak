<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1.0, user-scalable=no"/>
        <link rel="stylesheet" type="text/css" href="/static/foundation-6/css/foundation.min.css">
        <link rel="stylesheet" type="text/css" href="/static/erpblok.css">
        <title>${title}</title>
    </head>
    <body>
        <header></header>
        <main>
            <div class="row">
                <div class="columns small-12 medium-8 medium-offset-2 large-4 large-offset-4">
                    <img src="/login/logo"></img>
                    <div class="section">
                        <div id="error" class="hide alert callout">
                        </div>
                        <label for="database">Database</label>
                        <select id="database">
                            % for db in databases:
                                % if db == database:
                                    <option value="${db}" selected>${db}</option> \
                                % else:
                                    <option value="${db}">${db}</option> \
                                % endif
                            % endfor
                        </select>
                        <label for="login">Login</label>
                        <input id="login" type="text" required class="validate"/>
                        <label for="password">Password</label>
                        <input id="password" type="password" required class="validate"/>
                        <a id="submit" class="button expanded" href="#">Login</a>
                        % if allow_database_manager:
                            <a href="/database/manager" class="left">Database manager</a>
                        % endif
                    </div>
                </div>
            </div>
        </main>
        <footer></footer>
        <script type="text/javascript" src="/static/jquery-2.1.3.min.js" ></script>
        <script type="text/javascript" src="/static/foundation-5/js/foundation.min.js"></script>
        <script type="text/javascript" src="/static/login.js" ></script>
    </body>
</html>
