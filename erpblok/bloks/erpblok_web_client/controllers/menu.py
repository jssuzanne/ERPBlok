from anyblok import Declarations


register = Declarations.register
PyramidJsonRPC = Declarations.PyramidJsonRPC


@register(PyramidJsonRPC)
class Menus:

    @PyramidJsonRPC.rpc_method()
    def menusTree(self, menu=None, **kwargs):
        res = {'mainmenu': None, 'nodemenu': [], 'activemenu': None}
        Menu = self.registry.Web.Menu

        def recurse_parent(node):
            if node.parent:
                res['nodemenu'].append(node.id)
                recurse_parent(node.parent)
            else:
                res['mainmenu'] = node.id

        query = Menu.query().filter(Menu.id == menu)
        if query.count():
            m = query.first()
            if m.function or m.action:
                res['activemenu'] = m.id

            if m.parent:
                recurse_parent(m.parent)
            else:
                res['mainmenu'] = m.id

        return res


PyramidJsonRPC.add_route(PyramidJsonRPC.Menus, '/web/client/menus')
