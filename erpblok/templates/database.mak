<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <link rel="stylesheet" type="text/css" href="/static/database.css">
        <script type="text/javascript" src="/static/jquery-2.1.3.min.js" ></script>
        <script type="text/javascript" src="/static/database.js" ></script>
        <title>${title}</title>
    </head>
    <body>
        <nav>
            <ul>
                <li><a id="create" class="selected">Create a new database</a></li>
                <li><a id="drop">Drop an existing database</a></li>
                <li><a href="/" id="close">Close</a></li>
            </ul>
        </nav>
        <div class="page">
            <div id="create">
                <div id="error" class="invisible error centerize">
                    The database already exist
                </div>
                <div>
                    <label for="database">Name of the database</label>
                    <input id="database" type="text" name="database" required/>
                </div>
                <div>
                    <label for="login">Login of the administrator</label>
                    <input id="login" type="text" name="login" required/>
                </div>
                <div>
                    <label for="password">Password of the administrator</label>
                    <input id="password" type="text" name="password" required/>
                </div>
                <div class="centerize">
                    <input id="submit-create" type="button" value="Create" >
                </div>
            </div>
            <div id="drop" class="invisible">
                <div id="select">
                </div>
                <div class="centerize">
                    <input id="submit-drop" type="button" value="Drop" >
                </div>
            </div>
        </div>
    </body>
</html>
