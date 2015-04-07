from anyblok import Declarations


@Declarations.register(Declarations.Model)
class UI:
    pass


from . import template  # noqa
from . import action  # noqa
from . import menu  # noqa
from . import view  # noqa
