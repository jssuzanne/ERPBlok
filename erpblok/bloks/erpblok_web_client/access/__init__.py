from anyblok import Declarations, reload_module_if_blok_is_reloading


@Declarations.register(Declarations.Model)
class Access:
    pass


from . import group  # noqa
reload_module_if_blok_is_reloading(group)
from . import user  # noqa
reload_module_if_blok_is_reloading(user)
