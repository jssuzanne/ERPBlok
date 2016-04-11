from anyblok import Declarations
import pyramid.httpexceptions as exc


#register = Declarations.register
#PyramidJsonRPC = Declarations.PyramidJsonRPC
#
#
#@register(PyramidJsonRPC)
#class SideMenu:
#
#    @PyramidJsonRPC.rpc_method()
#    def openMenu(self, menu=None, **kwargs):
#        """ Return the main information for a specific menu in case of
#        open the accordion menu, add active class one the rigth menu and
#        the action or function to user"""
#        res = dict(nodemenu=[], activemenu=None, action=None)
#        try:
#            Menu = self.registry.UI.Menu
#
#            def recurse_parent(node):
#                res['nodemenu'].append(node.id)
#                if node.parent:
#                    recurse_parent(node.parent)
#
#            m = Menu.query().filter(Menu.id == menu).one_or_none()
#            if m:
#                if m.action:
#                    res['activemenu'] = m.id
#                    res['action'] = m.action.id
#                    if m.parent:
#                        recurse_parent(m.parent)
#
#            return res
#        except Exception as e:
#            return exc.HTTPInternalServerError(str(e))
#
#
#PyramidJsonRPC.add_route(PyramidJsonRPC.SideMenu, '/client/space/menu')
