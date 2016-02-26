from anyblok import Declarations

register = Declarations.register
PyramidHTTP = Declarations.PyramidHTTP


PyramidHTTP.add_route('client_space_description',
                      '/client/space/description',
                      request_method='POST')


PyramidHTTP.add_route('client_space_menus',
                      '/client/space/menus',
                      request_method='POST')


@register(PyramidHTTP)
class User:

    @PyramidHTTP.view(renderer='json')
    def client_space_description(self, space=None):
        return self.registry.Web.Space.query().get(space).get_description()

    @PyramidHTTP.view(renderer='json')
    def client_space_menus(self):
        return self.registry.Web.Space.Category.get_descriptions()
