from anyblok import Declarations


@Declarations.register(Declarations.Model)
class UI:
    pass


from . import menu  # noqa
