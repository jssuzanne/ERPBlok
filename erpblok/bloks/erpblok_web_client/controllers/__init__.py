from anyblok import reload_module_if_blok_is_reloading


from . import menu  # noqa
reload_module_if_blok_is_reloading(menu)
from . import action  # noqa
reload_module_if_blok_is_reloading(action)
from . import view  # noqa
reload_module_if_blok_is_reloading(view)
from . import field  # noqa
reload_module_if_blok_is_reloading(field)
