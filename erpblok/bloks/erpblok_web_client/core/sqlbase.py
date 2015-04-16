from anyblok import Declarations
from sqlalchemy.sql import functions


@Declarations.register(Declarations.Core)
class SqlBase:

    def field_render(self):
        """ Return list [primary keys, human render ] """
        return (self.to_primary_keys(), self.field_human_render())

    def field_human_render(self):
        """ Display value to be read and understand by human """
        return str(self.to_primary_keys())

    @classmethod
    def fields_description(cls):
        """ Return the information of the Field, Column, RelationShip """
        Field = cls.registry.System.Field
        Column = cls.registry.System.Column
        RelationShip = cls.registry.System.RelationShip

        def get_query(Model):
            columns = [
                Model.name.label('id'),
                Model.label,
                Model.ftype.label('type'),
            ]
            if Model is Column:
                columns.append(Model.nullable)
                columns.append(Model.primary_key)
                columns.append(functions.literal_column('null').label(
                    'model'))
            elif Model is RelationShip:
                columns.append(Model.nullable)
                columns.append(functions.literal_column('false').label(
                    'primary_key'))
                columns.append(Model.remote_model.label('model'))
            elif Model is Field:
                columns.append(
                    functions.literal_column('true as nullable'))
                columns.append(functions.literal_column('false').label(
                    'primary_key'))
                columns.append(functions.literal_column('null').label(
                    'model'))

            return Model.query(*columns).filter(
                Model.model == cls.__registry_name__)

        query = get_query(RelationShip).union_all(get_query(Column)).union_all(
            get_query(Field))
        fields2get = ['id', 'label', 'type', 'nullable', 'primary_key',
                      'model']
        return {x.id: {y: getattr(x, y) for y in fields2get}
                for x in query.all()}
