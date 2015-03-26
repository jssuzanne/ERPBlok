<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1.0, user-scalable=no"/>
        <title>${title}</title>
        % for x in css:
            <link rel="stylesheet" type="text/css" href="${x}" ></link>
        % endfor
        % for x in js:
            <script type="text/javascript" src="${x}" ></script>
        % endfor
    </head>
    <body class="application">
        <header>
            <ul id="dropdown-quickmenu" class="dropdown-content">
                <div class="row">
                    % for function, action, menu, icon, titlelabel in quickmenu:
                            <div class="col s4 m4 l4">
                        <li>
                                <a
                                    % if function:
                                        data-function="${function}"
                                    % endif
                                    % if menu:
                                        href="#menu=${menu}"
                                    % endif
                                    % if action:
                                        data-action="${action}"
                                    % endif
                                    % if title:
                                        title="${titlelabel}"
                                    % endif
                                >
                                    <i class="${icon}"></i>
                                </a>
                        </li>
                            </div>
                    % endfor
                </div>
            </ul>
            <ul id="dropdown-usermenu" class="dropdown-content">
                % for function, action, icon, name in usermenu:
                    <li>
                        <a
                            % if function:
                                data-function="${function}"
                            % endif
                            % if action:
                                data-action="${action}"
                            % endif
                        >${name}
                            % if icon:
                                <i class="left ${icon}"></i>
                            % endif
                        </a>
                    </li>
                % endfor
            </ul>
            <nav>
                <div class="nav-wrapper">
                    <ul class="left">
                        <li>
                            <a href="#" data-activates="slide-out" class="button-collapse">
                                <i class="mdi-navigation-menu"></i>
                            </a>
                        </li>
                    </ul>
                    <ul class="right">
                        <li>
                            <a class="dropdown-button" data-activates="dropdown-quickmenu">
                                <i class="mdi-navigation-apps left"></i>
                            </a>
                        </li>
                        <li>
                            <a class="dropdown-button" data-activates="dropdown-usermenu">User setting
                                <i class="mdi-navigation-arrow-drop-down right"></i>
                            </a>
                        </li>
                    </ul>
                </div>
                <ul id="slide-out" class="side-nav fixed">
                    <li>
                        <img class="responsive-img" src="/login/logo"><img>
                    </li>
                    ${add_menus(appmenu)}
                </ul>
            </nav>
        </header>
        <main>
            <div id="breadcrumb">
                <ul>
                </ul>
            </div>
            <div id="action-manager">
            </div>
        </main>
        <footer></footer>
    </body>
</html>
<%def name="add_menus(menus)">
    % for menu, name, submenus, in menus:
        % if submenus:
            <li>
                <label for="input-${menu}">${name}</label>
                <input type="checkbox" id="input-${menu}" />
                    <ul>
                        ${add_menus(submenus)}
                    </ul>
            </li>
        % else:
            <li>
                <a id="menu-${menu}" href="#menu=${menu}"><label>${name}<label></a>
            </li>
        % endif
    % endfor
</%def>
