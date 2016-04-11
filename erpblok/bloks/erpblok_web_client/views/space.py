import pyramid.httpexceptions as exc
from pyramid.view import view_config, view_defaults
from anyblok_pyramid import current_blok


@view_defaults(renderer='json', installed_blok=current_blok())
class Space:

    def __init__(self, request):
        self.request = request
        self.registry = request.anyblok.registry

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

    @view_config(route_name='client_space_description')
    def client_space_description(self):
        params = dict(self.request.params)
        space = params.get('space')
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
                "You can not acces at the space's category: %s" % (
                    category.label))

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

    @view_config(route_name='client_space_menus')
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
