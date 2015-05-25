from anyblok import Declarations, reload_module_if_blok_is_reloading


@Declarations.register(Declarations.Model)
class UI:
    pass


from . import template
reload_module_if_blok_is_reloading(template)
from . import action
reload_module_if_blok_is_reloading(action)
from . import menu
reload_module_if_blok_is_reloading(menu)
from . import view
reload_module_if_blok_is_reloading(view)
from . import transition
reload_module_if_blok_is_reloading(transition)
from . import button
reload_module_if_blok_is_reloading(button)
from . import image
reload_module_if_blok_is_reloading(image)
