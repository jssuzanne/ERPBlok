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
    <body>
        <div class="off-canvas-wrap" data-offcanvas="">
            <div class="inner-wrap">
                <nav class="top-bar hide-for-small" data-topbar role="navigation" data-options="is_hover: false">
                    <ul class="title-area">
                        <li class="name">
                            <h1><a href="#">${title}</a></h1>
                        </li>
                    </ul>
                    <section class="top-bar-section">
                        <ul class="right">
                            <li class="divider"></li>
                            ${top_nav_menus()}
                        </ul>
                    </section>
                </nav>
                <nav class="tab-bar show-for-small">
                    <section class="left-small">
                        <a class="left-off-canvas-toggle menu-icon" href="#"><span></span></a>
                    </section>
                    <section class="middle tab-bar-section">
                        <h1 class="title">${title}</h1>
                    </section>
                    <section class="right-small">
                        <a class="right-off-canvas-toggle menu-icon" href="#"><span></span></a>
                    </section>
                </nav>
                <aside class="left-off-canvas-menu">
                    <ul class="off-canvas-list accordion slide-out" data-accordion>
                        ${add_side_menus(appmenu)}
                    </ul>
                </aside>
                <aside class="right-off-canvas-menu">
                    <ul class="off-canvas-list">
                        ${top_nav_menus()}
                    </ul>
                </aside>
                <a class="exit-off-canvas" href="#"/>
                <section role="main" class="scroll-container">
                    <div class="row">
                         <div class="columns large-3 medium-4">
                            <div class="hide-for-small">
                                <div class="sidebar">
                                    <img src="/login/logo"/>
                                    <ul class="accordion slide-out" data-accordion>
                                        ${add_side_menus(appmenu)}
                                    </ul>
                                </div>
                            </div>
                        </div>
                        <div class="columns large-9 medium-8">
                            <div id="breadcrumb" class="breadcrumbs">
                            </div>
                            <div id="action-manager">
                            </div>
                        </div>
                    </div>
                </section>
            </div>
        </div>
    </body>
</html>
<%def name="add_side_menus(menus)">
     % for menu, name, submenus, in menus:
        <li class="accordion-navigation">
            % if submenus:
                <a id="amenu${menu}" href="#menu${menu}">${name}</a>
                <div id="menu${menu}" class="content">
                    <ul class="accordion" data-accordion>
                        ${add_side_menus(submenus)}
                    </ul>
                </div>
            % else:
                <a id="menu${menu}" href="#menu=${menu}" class="side-menu">${name}</a>
            % endif
        </li>
    % endfor
</%def>
<%def name="top_nav_menus()">
    % if quickmenu:
        <li class="hide-for-small">
            <div id="dropdown-quickmenu" class="icon-bar menu-icon">
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
                    >
                        <img src="${icon}"/>
                    </a>
                % endfor
            </div>
        </li>
        <li class="hide-for-small divider"/>
        <li class="has-dropdown show-for-small">
            <a class="menu-icon">Plop</a>
            <ul id="dropdown-quickmenu" class="dropdown small-block-grid-3 medium-block-grid-3 large-block-grid-3">
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
                        >
                            <img class="menu-img" src="${icon}"/>
                        </a>
                    </li>
                % endfor
            </ul>
        </li>
    % endif
    <li class="has-dropdown">
        <a href="#">User setting</a>
        <ul id="dropdown-usermenu" class="dropdown">
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
                            ><img src="${icon}" class="menu-img"/>${name}
                        % else:
                            >${name}
                        % endif
                    </a>
                </li>
            % endfor
        </ul>
    </li>
</%def>
