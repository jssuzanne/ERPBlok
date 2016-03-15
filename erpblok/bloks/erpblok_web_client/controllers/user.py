from anyblok import Declarations

register = Declarations.register
PyramidHTTP = Declarations.PyramidHTTP


PyramidHTTP.add_route('client_user_description',
                      '/client/user/description',
                      request_method='POST')


PyramidHTTP.add_route('client_user_menus',
                      '/client/user/menus',
                      request_method='POST')


@register(PyramidHTTP)
class User:

    @PyramidHTTP.view(renderer='json')
    def client_user_description(self, **kwargs):
        user_id = self.request.session['user_id']
        return self.registry.Web.User.query().get(user_id).get_description()

    @PyramidHTTP.view(renderer='json')
    def client_user_menus(self, **kwargs):
        user_id = self.request.session['user_id']
        return self.registry.Web.User.query().get(user_id).get_menus()
