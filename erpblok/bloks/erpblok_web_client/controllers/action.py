from anyblok import Declarations


register = Declarations.register
PyramidJsonRPC = Declarations.PyramidJsonRPC


@register(PyramidJsonRPC)
class Action:

    @PyramidJsonRPC.rpc_method()
    def load(self, action=None, **kwargs):
        action = int(action)
        form = """
            <div>
                <label for="login">Login</label>
                <div id="login"></div>
                <label for="password">Password</label>
                <div id="password"></div>
            </div>
        """
        views = [
            {
                'id': 1,
                'selectable': True,
                'mode': 'List',
                'primary_keys': ['login'],
                'fields': ['login', 'password'],
                'fields2display': ['login', 'password'],
                'headers': [
                    [{'id': 'login',
                      'label': 'Login',
                      'colspan': 1,
                      'rowspan': 1},
                     {'id': 'password',
                      'label': 'Password',
                      'colspan': 1,
                      'rowspan': 1}],
                ],
                'transitions': {
                    'selectRecord': ('open_view', 2),
                },
            },
            {
                'id': 2,
                'mode': 'Form',
                'template': form,
                'primary_keys': ['login'],
                'fields': ['login', 'password'],
            },
        ]
        res = {
            1: {
                'model': 'Model.UI.Login',
                'id': 1,
                'label': 'Super Plop',
                'dialog': False,
                'views': views,
                'selected': 1,
            },
            2: {
                'model': 'Model.UI.Login',
                'id': 3,
                'label': "Mr Titi",
                'dialog': True,
                'views': views,
            },
        }
        return res[action]


PyramidJsonRPC.add_route(PyramidJsonRPC.Action, '/web/client/action')
