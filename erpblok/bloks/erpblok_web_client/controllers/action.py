from anyblok import Declarations


register = Declarations.register
PyramidJsonRPC = Declarations.PyramidJsonRPC


@register(PyramidJsonRPC)
class Action:

    @PyramidJsonRPC.rpc_method()
    def load(self, action=None, **kwargs):
        list_ = """
            <table class="striped responsive-table">
                <thead>
                    <tr>
                        <th>Login</th>
                        <th>Password</th>
                    </tr>
                </thead>
                <tbody>
                </tbody>
            </table>
        """
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
                'mode': 'List',
                'template': list_,
                'primary_keys': ['login'],
                'fields': ['login', 'password'],
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
