from anyblok import Declarations
from sqlalchemy import or_, func
upper = func.upper


@Declarations.register(Declarations.Core)
class SqlBase:

    x2One_columns = []

    def __str__(self):
        return str(self.to_primary_keys())

    def field_render(self):
        """ Display value to be read and understand by human """
        cls = self.__class__
        columns = cls.x2One_columns
        if not columns:
            Column = cls.registry.System.Column
            columns = Column.query()
            columns = columns.filter(
                Column.model == cls.__registry_name__,
                Column.ftype.in_(['String', 'uString', 'Text', 'uText']))
            columns = columns.all().name

        if not columns:
            return str(self)

        return ', '.join([getattr(self, column)
                          for column in columns
                          if getattr(self, column)])

    @classmethod
    def x2One_search(cls, value):
        columns = cls.x2One_columns
        if not columns:
            Column = cls.registry.System.Column
            columns = Column.query()
            columns = columns.filter(
                Column.model == cls.__registry_name__,
                Column.ftype.in_(['String', 'uString', 'Text', 'uText']))
            columns = columns.all().name

        filters = []
        for column in columns:
            filters.append(upper(getattr(cls, column)).ilike(
                '%' + value + '%'))

        filters = or_(*filters)
        entries = cls.query().filter(filters).all()
        return [(entry.to_primary_keys(), entry.field_render())
                for entry in entries]
