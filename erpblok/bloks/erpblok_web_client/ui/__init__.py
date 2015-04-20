from anyblok import Declarations, reload_module_if_blok_is_reloaded


@Declarations.register(Declarations.Model)
class UI:
    pass


from . import template
reload_module_if_blok_is_reloaded(template)
from . import action
reload_module_if_blok_is_reloaded(action)
from . import menu
reload_module_if_blok_is_reloaded(menu)
from . import view
reload_module_if_blok_is_reloaded(view)
from . import transition
reload_module_if_blok_is_reloaded(transition)
from . import button
reload_module_if_blok_is_reloaded(button)
from . import image
reload_module_if_blok_is_reloaded(image)
