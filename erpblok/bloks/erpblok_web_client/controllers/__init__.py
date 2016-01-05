from anyblok import reload_module_if_blok_is_reloading


from . import menu
reload_module_if_blok_is_reloading(menu)
from . import action
reload_module_if_blok_is_reloading(action)
from . import view
reload_module_if_blok_is_reloading(view)
from . import field
reload_module_if_blok_is_reloading(field)
