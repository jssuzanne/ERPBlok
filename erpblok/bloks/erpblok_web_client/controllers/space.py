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

    @PyramidHTTP.view(renderer='json')
    def client_space_description(self, space=None):
        user_id = self.request.session['user_id']
        user = self.registry.Web.User.query().get(user_id)
        space = self.registry.Web.Space.query().get(space)
        if space.groups and not user.has_groups(space.groups.name):
            raise

        category = space.category
        if category.groups and not user.has_groups(category.groups.name):
            raise exc.HTTPForbidden()

        return space.get_description()

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
