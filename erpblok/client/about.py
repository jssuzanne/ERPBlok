from anyblok import Declarations


Declarations.Pyramid.add_route('about', '/about', request_method='POST')


@Declarations.Pyramid.add_view('about',
                               renderer='erpblok:templates/about.mak')
def get_about(request, database=None):
    return {}
