from anyblok import Declarations


@Declarations.register(Declarations.Model)
class UI:
    pass


from . import template  # noqa
from . import menu  # noqa
