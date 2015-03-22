from anyblok import Declarations


register = Declarations.register
Web = Declarations.Model.Web
Integer = Declarations.Column.Integer
String = Declarations.Column.String


@register(Web)
class Login:

    id = Integer(primary_key=True)
    login = String(nullable=False)
    password = String(nullable=False)

    @classmethod
    def update_admin(cls, login, password):
        user = cls.registry.IO.Mapping.get('Model.Access.User',
                                           'main_admin_user')
        user.login.login = login
        user.login.password = password

    @classmethod
    def check_authentification(cls, login, password):
        query = cls.query().filter(cls.login == login)
        query = query.filter(cls.password == password)
        if query.count():
            return True
        else:
            return False
