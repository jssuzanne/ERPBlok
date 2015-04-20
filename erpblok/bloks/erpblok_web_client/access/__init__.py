from anyblok import Declarations, reload_module_if_blok_is_reloaded


@Declarations.register(Declarations.Model)
class Access:
    pass


from . import group
reload_module_if_blok_is_reloaded(group)
from . import user
reload_module_if_blok_is_reloaded(user)
