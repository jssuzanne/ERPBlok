from anyblok import Declarations


@Declarations.register(Declarations.Core)
class SqlBase:

    def __str__(self):
        return str(self.to_primary_keys())

    def field_render(self):
        """ Display value to be read and understand by human """
        return str(self)
