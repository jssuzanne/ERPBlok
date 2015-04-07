from anyblok import Declarations


register = Declarations.register
PyramidJsonRPC = Declarations.PyramidJsonRPC


@register(PyramidJsonRPC)
class SideMenu:

    @PyramidJsonRPC.rpc_method()
    def openMenu(self, menu=None, **kwargs):
        res = dict(nodemenu=[], activemenu=None, action=None, function=None)
        Menu = self.registry.UI.Menu

        def recurse_parent(node):
            res['nodemenu'].append(node.id)
            if node.parent:
                recurse_parent(node.parent)

        query = Menu.query().filter(Menu.id == menu)
        if query.count():
            m = query.first()
            if m.function or m.action:
                res['activemenu'] = m.id
                if m.function:
                    res['function'] = m.function

                if m.action:
                    res['action'] = m.action.render()

                if m.parent:
                    recurse_parent(m.parent)

        return res


PyramidJsonRPC.add_route(PyramidJsonRPC.SideMenu, '/web/client/side/menu')
