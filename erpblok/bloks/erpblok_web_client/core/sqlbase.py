from anyblok import Declarations


@Declarations.register(Declarations.Core)
class SqlBase:

    def field_render(self):
        return (self.to_primary_keys(), self.field_human_render())

    def field_human_render(self):
        return str(self.to_primary_keys())
