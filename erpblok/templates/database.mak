<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1.0, user-scalable=no"/>
        <link rel="stylesheet" type="text/css" href="/static/foundation-5/css/foundation.min.css">
        <link rel="stylesheet" type="text/css" href="/static/erpblok.css">
        <title>${title}</title>
    </head>
    <body>
        <div class="off-canvas-wrap" data-offcanvas="">
            <div class="inner-wrap">
                <nav class="top-bar hide-for-small" data-topbar>
                    <ul class="title-area">
                        <li class="name">
                            <h1>
                                <a>Database manager</a>
                            </h1>
                        </li>
                    </ul>
                </nav>
                <nav class="tab-bar show-for-small">
                    <a class="left-off-canvas-toggle menu-icon" role="button">
                        <span></span>
                    </a>
                    <section class="right tab-bar-section">
                        <h1 class="title">DB Manager</h1>
                    </section>
                </nav>
                <aside class="left-off-canvas-menu">
                    ${display_menu()}
                </aside>
                <a class="exit-off-canvas" href="#"/>
                <section role="main" class="scroll-container">
                    <div class="row">
                        <div class="columns large-3 medium-4">
                            <div class="hide-for-small">
                                <div class="sidebar">
                                    <img src="/login/logo"/>
                                    ${display_menu()}
                                </div>
                            </div>
                        </div>
                        <div class="columns large-8 medium-6">
                            <div id="error" data-alert class="hide alert-box alert radius text-center">
                                The database already exist
                            </div>
                            <div id="error2" data-alert class="hide alert-box alert radius text-center">
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
                                <a id="submit-create" class="button right radius" href="#">Create</a>
                            </div>
                            <div id="drop" class="hide">
                                <div id="select">
                                </div>
                                <a id="submit-drop" class="button right radius" href="#">Drop</a>
                            </div>
                        </div>
                    </div>
                </section>
            </div>
        </div>
        <script type="text/javascript" src="/static/jquery-2.1.3.min.js" ></script>
        <script type="text/javascript" src="/static/foundation-5/js/foundation.min.js"></script>
        <script type="text/javascript" src="/static/database.js" ></script>
    </body>
</html>
<%def name="display_menu()">
    <nav>
        <ul class="side-nav" role="navigation">
            <li role="menuitem" class="active" id="create">
                <a>Create a new database</a>
            </li>
            <li role="menuitem" id="drop">
                <a>Drop an existing database</a>
            </li>
            <li role="menuitem" role="menuitem">
                <a href="/">Close</a>
            </li>
        </ul>
    </nav>
</%def>
