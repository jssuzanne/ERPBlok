<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1.0, user-scalable=no"/>
        <link rel="stylesheet" type="text/css" href="/static/materialize-src/css/materialize.css">
        <link rel="stylesheet" type="text/css" href="/static/erpblok.css">
        <script type="text/javascript" src="/static/jquery-2.1.3.min.js" ></script>
        <script type="text/javascript" src="/static/materialize-src/js/bin/materialize.min.js"></script>
        <script type="text/javascript" src="/static/login.js" ></script>
        <title>${title}</title>
    </head>
    <body>
        <header></header>
        <main>
            <div class="valign-wrapper">
                <div class="container">
                    <div class="row">
                        <div class="col s12 m8 offset-m2 l4 offset-l4">
                            <img class="responsive-img" src="/login/logo"></img>
                            <div class="section">
                                <div id="error" class="hide error center-align">
                                </div>
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
                                <label for="login">Login</label>
                                <input id="login" type="text" required class="validate"/>
                                <label for="password">Login</label>
                                <input id="password" type="password" required class="validate"/>
                                % if allow_database_manager:
                                    <a href="/database/manager" class="left">Database manager</a>
                                % endif
                                <a id="submit"
                                    class="waves-effect waves-light btn right" >Login</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>
        <footer></footer>
    </body>
</html>
