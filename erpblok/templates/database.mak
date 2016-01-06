<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1.0, user-scalable=no"/>
        <link rel="stylesheet" type="text/css" href="/static/foundation-6.1.0/css/foundation.min.css">
        <link rel="stylesheet" type="text/css" href="/static/erpblok.css">
        <title>${title}</title>
    </head>
    <body>
        <div class="off-canvas-wrapper">
            <div class="off-canvas-wrapper-inner" data-off-canvas-wrapper>
                <div class="off-canvas position-left" id="offCanvas" data-off-canvas>
                    ${display_menu()}
                </div>
                <div class="off-canvas-content" data-off-canvas-content>
                    <div class="top-bar hide-for-small-only">
                        <ul class="title-area">
                            <li class="name">
                                <h1>
                                    <a>Database manager</a>
                                </h1>
                            </li>
                        </ul>
                    </div>
                    <div class="title-bar show-for-small-only">
                        <div class="title-bar-left">
                            <button class="menu-icon" type="button" data-toggle="offCanvas"></button>
                            <span class="title-bar-title">DB Manager</span>
                        </div>
                    </div>
                    <section role="main" class="scroll-container">
                        <div class="row">
                            <div class="columns large-3 medium-4">
                                <div class="hide-for-small-only">
                                    <div class="sidebar">
                                        <img src="/login/logo"/>
                                        ${display_menu()}
                                    </div>
                                </div>
                            </div>
                            <div class="columns large-8 medium-6">
                                <div id="error" data-alert class="hide alert callout">
                                    The database already exist
                                </div>
                                <div id="error2" data-alert class="hide alert callout">
                                    The password and the confirmation of the password are different
                                </div>
                                <div id="error3" data-alert class="hide alert callout">
                                    Wrong database manager password
                                </div>
                                <label for="db_manager_password">Passord for database manager</label>
                                <input id="db_manager_password" type="password" required/>
                                <div id="create">
                                    <label for="database">Name of the database</label>
                                    <input id="database" type="text" required/>
                                    <label for="login">Login of the administrator</label>
                                    <input id="login" type="text" required value="admin">
                                    <label for="password">Password of the administrator</label>
                                    <input id="password" type="password" required/>
                                    <label for="password2">Confirm the password of the administrator</label>
                                    <input id="password2" type="password" required/>
                                    <input id="db_manager_blok_manager" type="checkbox" default-value="${blok_manager}"/>
                                    <label for="db_manager_blok_manager">Install blok manager</label>
                                    <br/>
                                    <input id="db_manager_demo" type="checkbox" default-value="${demo}"/>
                                    <label for="db_manager_demo">Install demo bloks</label>
                                    <br>
                                    <a id="submit-create" class="button expanded" href="#">Create</a>
                                </div>
                                <div id="drop" class="hide">
                                    <div id="select">
                                    </div>
                                    <a id="submit-drop" class="button expanded" href="#">Drop</a>
                                </div>
                            </div>
                        </div>
                    </section>
                </div>
            </div>
        </div>
        <script type="text/javascript" src="/static/jquery-2.1.3.min.js" ></script>
        <script type="text/javascript" src="/static/foundation-6.1.0/js/foundation.min.js"></script>
        <script type="text/javascript" src="/static/database.js" ></script>
    </body>
</html>
<%def name="display_menu()">
    <ul class="menu vertical">
        <li role="menuitem" id="create">
            <a class="is-active">Create a new database</a>
        </li>
        <li role="menuitem" id="drop">
            <a>Drop an existing database</a>
        </li>
        <li role="menuitem" role="menuitem">
            <a href="/">Close</a>
        </li>
    </ul>
</%def>
