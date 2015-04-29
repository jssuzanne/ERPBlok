from anyblok import Declarations


@Declarations.register(Declarations.Core)
class SqlBase:

    def field_render(self):
        """ Return list [primary keys, human render ] """
        return (self.to_primary_keys(), self.field_human_render())

    def field_human_render(self):
        """ Display value to be read and understand by human """
        return str(self.to_primary_keys())
