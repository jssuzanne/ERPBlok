from anyblok import Declarations, reload_module_if_blok_is_reloading


@Declarations.register(Declarations.Model)
class UI:
    pass


from . import template  # noqa
reload_module_if_blok_is_reloading(template)
from . import action  # noqa
reload_module_if_blok_is_reloading(action)
from . import menu  # noqa
reload_module_if_blok_is_reloading(menu)
from . import view  # noqa
reload_module_if_blok_is_reloading(view)
from . import transition  # noqa
reload_module_if_blok_is_reloading(transition)
from . import button  # noqa
reload_module_if_blok_is_reloading(button)
from . import image  # noqa
reload_module_if_blok_is_reloading(image)
