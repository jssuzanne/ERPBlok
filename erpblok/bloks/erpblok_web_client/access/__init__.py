from anyblok import Declarations


@Declarations.register(Declarations.Model)
class Access:
    pass


from . import group  # noqa
from . import user  # noqa
