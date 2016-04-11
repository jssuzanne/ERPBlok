from pyramid_rpc.jsonrpc import jsonrpc_method
from pyramid.view import view_defaults
from anyblok_pyramid import current_blok


@view_defaults(installed_blok=current_blok())
class Action:

    def __init__(self, request):
        self.request = request
        self.registry = request.anyblok.registry

    @jsonrpc_method(endpoint='web_client_action')
    def load(self, action=None):
        """ return the action render

        :param action: id of the action """
        user_id = self.request.session['user_id']
        user = self.registry.Web.User.query().get(user_id)
        UIAction = self.registry.UI.Action
        action = UIAction.query().filter(UIAction.id == int(action)).first()
        return action.render(user)
