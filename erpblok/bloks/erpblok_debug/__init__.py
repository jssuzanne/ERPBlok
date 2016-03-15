from anyblok.blok import Blok


class ERPBlokDebug(Blok):
    """ Demo blok for ERPBlok """
    version = '0.0.1'

    required = [
        'anyblok-io-xml',
        'erpblok-core',
    ]

    def update(self, latest_version):
        """ Update the database """
        self.import_file('xml', 'Model.UI.Action', 'action.xml')
        self.import_file('xml', 'Model.Web.Space', 'space.xml')

    def uninstall(self):
        data2remove_by_model = [
            ['Model.UI.Action', [
                "action_db_model",
                "action_db_field",
                "action_db_column",
                "action_db_rs",
                "action_ui_menu",
                "action_ui_action",
                "action_ui_view",
                "action_io_mapping",
                "action_io_importer",
                "action_io_exporter"]],
            ['Model.UI.Menu', [
                "menu_low_level_db_model",
                "menu_low_level_db_field",
                "menu_low_level_db_column",
                "menu_low_level_db_relationship",
                "menu_low_level_db",
                "menu_low_level_ui_menu",
                "menu_low_level_ui_action",
                "menu_low_level_ui_view",
                "menu_low_level_ui",
                "menu_low_level_io_mapper",
                "menu_low_level_io_importer",
                "menu_low_level_io_exporter",
                "menu_low_level_io"]],
            ['Model.Web.Space', ['setting_space_low_level']],
        ]
        Mapping = self.registry.IO.Mapping
        kwargs = {'mapping_only': False}
        for model, keys in data2remove_by_model:
            Mapping.multi_delete(model, *keys, **kwargs)
