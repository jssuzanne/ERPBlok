from anyblok import Declarations


register = Declarations.register
Web = Declarations.Model.Web
String = Declarations.Column.String


@register(Web)
class Login:

    login = String(primary_key=True)
    password = String(nullable=False)

    @classmethod
    def create_admin(cls, login, password):
        cls.insert(login=login, password=password)
        # TODO FIXME create user

    @classmethod
    def check_authentification(cls, login, password):
        query = cls.query().filter(cls.login == login)
        query = query.filter(cls.password == password)
        if query.count():
            return True
        else:
            return False
