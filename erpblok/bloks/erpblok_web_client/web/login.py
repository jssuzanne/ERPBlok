from anyblok import Declarations
from anyblok.column import Integer, String, Password, Boolean

register = Declarations.register
Web = Declarations.Model.Web


@register(Web)
class Login:

    id = Integer(primary_key=True)
    login = String(nullable=False, unique=True)
    password = Password(nullable=False, unique=True,
                        crypt_context={'schemes': ['md5_crypt']})
    active = Boolean(default=True)

    def __str__(self):
        return self.login

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
        query = query.filter(cls.active.is_(True))
        if query.count():
            for self in query.all():
                if self.password == password:
                    if self.user:
                        return self.user.id

        return False
