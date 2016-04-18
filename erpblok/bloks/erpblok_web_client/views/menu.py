import pyramid.httpexceptions as exc
from pyramid_rpc.jsonrpc import jsonrpc_method
from pyramid.view import view_defaults
from anyblok_pyramid import current_blok


@view_defaults(installed_blok=current_blok())
class SideMenu:

    def __init__(self, request):
        self.request = request
        self.registry = request.anyblok.registry

    @jsonrpc_method(endpoint='client_space_menu')
    def openMenu(self, menu=None):
        """ Return the main information for a specific menu in case of
        open the accordion menu, add active class one the rigth menu and
        the action or function to user"""
        res = dict(nodemenu=[], activemenu=None, action=None)
        try:
            Menu = self.registry.UI.Menu

            def recurse_parent(node):
                res['nodemenu'].append(node.id)
                if node.parent:
                    recurse_parent(node.parent)

            m = Menu.query().filter(Menu.id == menu).one_or_none()
            if m:
                if m.action:
                    res['activemenu'] = m.id
                    res['action'] = m.action.id
                    if m.parent:
                        recurse_parent(m.parent)

            return res
        except Exception as e:
            return exc.HTTPInternalServerError(str(e))
