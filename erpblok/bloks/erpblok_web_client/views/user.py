from pyramid.view import view_config, view_defaults
from anyblok_pyramid import current_blok


@view_defaults(renderer='json', installed_blok=current_blok())
class User:

    def __init__(self, request):
        self.request = request
        self.registry = request.anyblok.registry

    @view_config(route_name='client_user_description')
    def client_user_description(self):
        user_id = self.request.session['user_id']
        return self.registry.Web.User.query().get(user_id).get_description()

    @view_config(route_name='client_user_menus')
    def client_user_menus(self):
        user_id = self.request.session['user_id']
        return self.registry.Web.User.query().get(user_id).get_menus()
