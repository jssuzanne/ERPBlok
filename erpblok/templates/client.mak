<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <title>${title}</title>
        % for x in css:
            <link rel="stylesheet" type="text/css" href="${x}" ></link>
        % endfor
        % for x in js:
            <script type="text/javascript" src="${x}" ></script>
        % endfor
    </head>
    <body>
        <header>
        </header>
        <nav id="toolbar">
            <ul>
                % for id, name in mainmenu:
                    <li><a class="mainmenu" id="${id}">${name}</a></li>
                % endfor
                <li class="right">
                    <a>User setting <span class="caret"></span></a>
                    <div>
                        <ul>
                            % for function, icon, name in usermenu:
                                <li>
                                    % if icon:
                                        <img src="${icon}" width="48" height="48"></img>
                                    % endif
                                    <a class="usermenu"
                                       data-function="${function}">${name}</a>
                                </li>
                            % endfor
                        </ul>
                    </div>
                </li>
                % if quickmenu:
                    <li class="right">
                        <a>Quick <span class="caret"></span></a>
                        <div class="quickmenu">
                            <ul>
                                % for function, action, menu, icon, titlelabel in quickmenu:
                                    <li>
                                        <a
                                            % if function:
                                                data-function="${function}"
                                            % endif
                                            % if action:
                                                data-action="${action}"
                                            % endif
                                            % if menu:
                                                data-menu="${menu}"
                                            % endif
                                            % if title:
                                                title="${titlelabel}"
                                            % endif
                                        >
                                           <img src="${icon}" width="48" height="48"></img>
                                        </a>
                                    </li>
                                % endfor
                            </ul>
                        </div>
                    </li>
                % endif
            </ul>
        </nav>
        <div id="body">
            <aside id="menus">
                % for parent, submenus in menus:
                    <nav id="menu-${parent}" class="invisible">
                        ${add_menus(submenus)}
                    </nav>
                % endfor
            </aside>
            <section id="application">
                TODO, next Step
            </section>
        </div>
        <footer>
        </footer>
    </body>
</html>
<%def name="add_menus(menus)">
    <ol>
        % for function, action, menu, name , submenus, in menus:
            % if submenus:
                <li id="menu-${menu}">
                    <label for="input-${menu}">${name}</label>
                    <input type="checkbox" id="input-${menu}" />
                    ${add_menus(submenus)}
                </li>
            % else:
                <li id="menu-${menu}" class="sheet">
                    <a
                        % if function:
                            data-function="${function}"
                        % endif
                        % if action:
                            data-action="${action}"
                        % endif
                        % if menu:
                            data-menu="${menu}"
                        % endif
                        >${name}</a>
                </li>
            % endif
        % endfor
    </ol>
</%def>
