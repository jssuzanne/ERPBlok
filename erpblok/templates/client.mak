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
        <div class="off-canvas-wrapper">
            <div class="off-canvas-wrapper-inner" data-off-canvas-wrapper>
                <div class="off-canvas position-left" id="offCanvasLeft" data-off-canvas>
                    <ul class="menu vertical nested side-menu" id="accordion-menu-small">
                        ${add_side_menus(appmenu)}
                    </ul>
                </div>
                <div class="off-canvas position-right" id="offCanvasRight" data-off-canvas data-position="right">
                    <ul class="menu vertical" id="topbar-menu-small">
                        ${top_nav_menus_quick_small()}
                        ${top_nav_menus_user_small()}
                        <li><a class="button logout">Log out</a></li>
                    </ul>
                </div>
                <div class="off-canvas-content" data-off-canvas-content>
                    <div class="title-bar">
                        <div class="title-bar-left">
                            <div class="show-for-large">
                                <button class="menu-icon toggle-menu" type="button"></button>
                                <span class="title-bar-title">${title}</span>
                            </div>
                            <div class="hide-for-large">
                                <button class="menu-icon" type="button" data-toggle="offCanvasLeft"></button>
                                <span class="title-bar-title">${title}</span>
                            </div>
                        </div>
                        <div class="title-bar-right">
                            <div class="show-for-large">
                                <ul class="dropdown menu" id="topbar-menu-large" data-dropdown-menu>
                                    ${top_nav_menus_quick_large()}
                                    ${top_nav_menus_user_large()}
                                    <li><a class="button logout">Log out</a></li>
                                </ul>
                            </div>
                            <div class="hide-for-large">
                                <button class="menu-icon" type="button" data-toggle="offCanvasRight"></button>
                            </div>
                        </div>
                    </div>
                    <section role="main" class="scroll-container">
                        <div class="row">
                             <div id="main-menu" class="columns large-3 show-for-large">
                                <div>
                                    <div class="sidebar">
                                        <ul class="menu vertical nested side-menu" id="accordion-menu-large">
                                            ${add_side_menus(appmenu)}
                                        </ul>
                                    </div>
                                </div>
                            </div>
                            <div id="main-app" class="columns large-9">
                                <nav role="navigation">
                                    <ul id="breadcrumb" class="breadcrumbs">
                                    </ul>
                                </nav>
                                <div id="action-manager">
                                </div>
                            </div>
                        </div>
                    </section>
                </div>
            </div>
        </div>
        % for x in js:
            <script type="text/javascript" src="${x}" ></script>
        % endfor
        ${templates | n}
    </body>
</html>
<%def name="add_side_menus(menus)">
     % for menu, name, submenus, in menus:
        <li class="side-menu-${menu}">
            % if submenus:
                <a href="#menu${menu}">${name}</a>
                <ul class="menu vertical nested side-menu-${menu}">
                    ${add_side_menus(submenus)}
                </ul>
            % else:
                <a id="menu${menu}" href="#menu=${menu}&clean-breadcrumbs=1">${name}</a>
            % endif
        </li>
    % endfor
</%def>
<%def name="top_nav_menus_quick_large()">
    % if quickmenu:
        <li>
            <div id="dropdown-quickmenu" class="menu">
                % for function, action, menu, icon, titlelabel in quickmenu:
                    <a class="item"
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
                        ><i class="${icon}"></i>
                    </a>
                % endfor
            </div>
        </li>
    % endif
</%def>
<%def name="top_nav_menus_quick_small()">
    % if quickmenu:
        <li>
            <a>Quick menus</a>
            <ul id="dropdown-quickmenu" class="menu small-block-grid-3 medium-block-grid-3 large-block-grid-3">
                % for function, action, menu, icon, titlelabel in quickmenu:
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
                        ><i class="${icon}"></i>
                        </a>
                    </li>
                % endfor
            </ul>
        </li>
    % endif
</%def>
<%def name="top_nav_menus_user_large()">
    <li>
        <a href="#">${username}</a>
        <ul id="dropdown-usermenu" class="menu">
            % for function, action, icon, name in usermenu:
                <li>
                    <a
                        % if function:
                            data-function="${function}"
                        % endif
                        % if action:
                            data-action="${action}"
                        % endif
                        % if icon:
                            ><i class="${icon}"></i>${name}
                        % else:
                            >${name}
                        % endif
                    </a>
                </li>
            % endfor
        </ul>
    </li>
</%def>
<%def name="top_nav_menus_user_small()">
    <li>
        <a href="#">${username}</a>
        <ul id="dropdown-usermenu" class="menu vertical">
            % for function, action, icon, name in usermenu:
                <li>
                    <a
                        % if function:
                            data-function="${function}"
                        % endif
                        % if action:
                            data-action="${action}"
                        % endif
                        % if icon:
                            ><i class="${icon}"></i>${name}
                        % else:
                            >${name}
                        % endif
                    </a>
                </li>
            % endfor
        </ul>
    </li>
</%def>
