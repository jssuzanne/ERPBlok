from anyblok import Declarations
from anyblok.column import Integer, String

register = Declarations.register
Web = Declarations.Model.Web


@register(Web)
class Login:

    id = Integer(primary_key=True)
    login = String(nullable=False)
    password = String(nullable=False)

    @classmethod
    def update_admin(cls, login, password):
        """ Change the login and password of the main administrator """
        user = cls.registry.IO.Mapping.get('Model.Access.User',
                                           'main_admin_user')
        user.login.login = login
        user.login.password = password

    @classmethod
    def check_authentification(cls, login, password):
        """ Verify if the login / password allow to found a user

        :param login: login of the user
        :param password: password of the use
        :rtype: Boolean True if the user is found else False
        """
        query = cls.query().filter(cls.login == login)
        query = query.filter(cls.password == password)
        if query.count():
            return True
        else:
            return False
