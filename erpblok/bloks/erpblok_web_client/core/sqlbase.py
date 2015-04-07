from anyblok import Declarations


@Declarations.register(Declarations.Core)
class SqlBase:

    def render(self):
        return self.to_primary_keys(), str(self)
