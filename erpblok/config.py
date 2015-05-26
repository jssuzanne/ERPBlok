# -*- coding: utf-8 -*-
from anyblok.config import Configuration


@Configuration.add('database-manager', label="Database manager")
def add_database(group, configuration):
    group.add_argument('--db-manager-password', dest='db_manager_password')
    group.add_argument('--db-manager-demo', dest='db_manager_demo',
                       action='store_true')
    group.add_argument('--db-manager-blok-manager',
                       dest='db_manager_blok_manager',
                       action='store_true')

    configuration.update({
        'db_manager_password': 'admin',
    })
