# -*- coding: utf-8 -*-
from anyblok.config import Configuration
from anyblok_pyramid import scripts  # noqa for update pyramid conf


Configuration.applications['pyramid']['configuration_groups'].append(
    'database-manager')
Configuration.applications['gunicorn']['configuration_groups'].append(
    'database-manager')


@Configuration.add('database-manager', label="Database manager")
def add_database(group):
    group.add_argument('--db-filter')
    group.add_argument('--db-manager-password', default='admin')
    group.add_argument('--db-manager-demo', action='store_true')
    group.add_argument('--db-manager-blok-manager', action='store_true')
