from anyblok import Declarations
import pyramid.httpexceptions as exc

register = Declarations.register
PyramidHTTP = Declarations.PyramidHTTP


PyramidHTTP.add_route('client_space_description',
                      '/client/space/description',
                      request_method='POST')


PyramidHTTP.add_route('client_space_menus',
                      '/client/space/menus',
                      request_method='POST')


@register(PyramidHTTP)
class Space:

    def define_menus_for(self, user, parents, menus):
        for menu in menus:
            if menu.groups and not user.has_groups(menu.groups):
                continue

            val = {
                'id': menu.id,
                'label': menu.label,
                'action': menu.action and menu.action.id or None,
                'children': [],
            }
            if menu.children:
                self.define_menus_for(user, val['children'], menu.children)

            parents.append(val)

    @PyramidHTTP.view(renderer='json')
    def client_space_description(self, space=None):
        user_id = self.request.session['user_id']
        user = self.registry.Web.User.query().get(user_id)
        _space = self.registry.Web.Space.query().get(space)
        if _space is None:
            return exc.HTTPNotFound(
                "The space (id = %s) is not found" % space)

        if _space.groups and not user.has_groups(_space.groups.name):
            return exc.HTTPForbidden(
                "You can not acces at the space: %s" % _space.label)

        category = _space.category
        if category.groups and not user.has_groups(category.groups.name):
            return exc.HTTPForbidden(
                "You can not acces at the space's category: %s" % category.label)

        res = {
            'id': _space.id,
            'label': _space.label,
            'icon': _space.icon,
            'menu_position': _space.menu_position,
            'menus': [],
        }
        if _space.menus:
            self.define_menus_for(user, res['menus'], _space.menus)

        if _space.default_menu:
            res['default_menu'] = _space.default_menu.id

        if _space.default_action:
            res['default_action'] = _space.default_action.id

        return res

    @PyramidHTTP.view(renderer='json')
    def client_space_menus(self):
        res = []
        user_id = self.request.session['user_id']
        user = self.registry.Web.User.query().get(user_id)
        Space = self.registry.Web.Space
        Category = Space.Category
        for category in Category.query().order_by(Category.order).all():
            if category.groups and not user.has_groups(category.groups.name):
                continue

            spaces = []
            query = Space.query().filter(Space.category == category)
            query = query.order_by(Space.order)
            for space in query.all():
                if space.groups and not user.has_groups(space.groups.name):
                    continue

                spaces.append({
                    'id': space.id,
                    'label': space.label,
                    'icon': space.icon,
                    'description': space.description,
                })

            if spaces:
                res.append({
                    'id': category.label,
                    'icon': category.icon,
                    'label': category.label,
                    'menus': spaces})

        return res
