from anyblok import reload_module_if_blok_is_reloaded


from . import menu
reload_module_if_blok_is_reloaded(menu)
from . import action
reload_module_if_blok_is_reloaded(action)
from . import view
reload_module_if_blok_is_reloaded(view)
