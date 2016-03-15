from anyblok.blok import Blok
from anyblok.config import Configuration


class ERPBlokBlokManager(Blok):
    """ Blok manager for ERPBlok """
    version = '0.0.1'

    required = [
        'anyblok-core',
        'anyblok-io-xml',
    ]

    setting_blok_description = {
        'label': 'Blok Manager',
        'description': 'Allow to install, update or unstall bloks from the '
                       'application',
        'value': Configuration.get('db_manager_blok_manager'),
    }

    views = [
        'blok.tmpl',
    ]

    def update(self, latest_version):
        """ Update the database """
        self.import_file('xml', 'Model.Web.Space', 'space.xml')

    def uninstall(self):
        data2remove_by_model = [
            ['Model.UI.Action.Button', [
                "buttons_blok_manager_reload_all_bloks"]],
            ['Model.UI.Action.ButtonGroup', [
                "group_button_blok_manager_other"]],
            ['Model.UI.Action.Transition', [
                "transition_blok_manager_select_record",
                "transition_blok_manager_new_record"]],
            ['Model.UI.View', [
                "view_blok_thumbnails",
                "view_blok_form"]],
            ['Model.Web.Space', ['setting_space_blok']],
            ['Model.UI.Action', ["action_setting_blok"]],
        ]
        Mapping = self.registry.IO.Mapping
        kwargs = {'mapping_only': False}
        for model, keys in data2remove_by_model:
            Mapping.multi_delete(model, *keys, **kwargs)

    @classmethod
    def import_declaration_module(cls):
        from . import blok  # noqa

    @classmethod
    def reload_declaration_module(cls, reload):
        from . import blok
        reload(blok)
