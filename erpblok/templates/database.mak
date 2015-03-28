<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1.0, user-scalable=no"/>
        <link rel="stylesheet" type="text/css" href="/static/foundation-5/css/foundation.min.css">
        <link rel="stylesheet" type="text/css" href="/static/erpblok.css">
        <script type="text/javascript" src="/static/jquery-2.1.3.min.js" ></script>
        <script type="text/javascript" src="/static/foundation-5/js/foundation.min.js"></script>
        <script type="text/javascript" src="/static/database.js" ></script>
        <title>${title}</title>
    </head>
    <body>
        <nav class="top-bar" data-topbar role="navigation">
            <ul class="title-area">
                <li class="name">
                    <h1>
                        <a>Database manager</a>
                    </h1>
                </li>
                <li class="toggle-topbar menu-icon"><a><span></span></a></li>
            </ul>
            <section class="top-bar-section">
                <ul class="left">
                    <li class="divider"/>
                    <li class="active" id="create">
                        <a>Create a new database</a>
                    </li>
                    <li id="drop">
                        <a>Drop an existing database</a>
                    </li>
                    <li role="menuitem">
                        <a href="/">Close</a>
                    </li>
                </ul>
            </section>
        </nav>
        <div class="row">
            <div class="columns large-offset-2 large-8 medium-offset-1 medium-10">
                <div id="error" data-alert class="hide alert-box alert round">
                    The database already exist
                </div>
                <div id="error2" data-alert class="hide alert-box alert round">
                    The password and the confirmation of the password are different
                </div>
                <div id="create">
                    <label for="database">Name of the database</label>
                    <input id="database" type="text" required/>
                    <label for="login">Login of the administrator</label>
                    <input id="login" type="text" required value="admin">
                    <label for="password">Password of the administrator</label>
                    <input id="password" type="password" required/>
                    <label for="password2">Confirm the password of the administrator</label>
                    <input id="password2" type="password" required/>
                    <a id="submit-create" class="button right radius">Create</a>
                </div>
                <div id="drop" class="hide">
                    <div id="select">
                    </div>
                    <a id="submit-drop" class="button right radius">Drop</a>
                </div>
            </div>
        </div>
    </body>
</html>
