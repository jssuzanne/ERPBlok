.. contents::

ERPBlok framework
=================

Homepage controller
-------------------

.. automodule:: erpblok.client.homepage

.. autofunction:: get_homepage
    :noindex:

Client controller
-----------------

.. automodule:: erpblok.client.web

.. autofunction:: load_client
    :noindex:

Login controllers
-----------------

.. automodule:: erpblok.client.login

.. autofunction:: get_login
    :noindex:

.. autofunction:: get_login_logo
    :noindex:

.. autofunction:: get_databases
    :noindex:

.. autofunction:: post_login_connect
    :noindex:

.. autofunction:: post_login_disconnect
    :noindex:

Database manager controllers
----------------------------

.. automodule:: erpblok.client.database

.. autofunction:: check_allow_database_manager
    :noindex:

.. autofunction:: check_db_manager_password
    :noindex:

.. autofunction:: get_database
    :noindex:

.. autofunction:: get_menus
    :noindex:

.. autofunction:: get_addons
    :noindex:

.. autofunction:: get_databases
    :noindex:

.. autofunction:: post_create_database
    :noindex:

.. autofunction:: post_drop_database
    :noindex:

.. autofunction:: post_list_database
    :noindex:

Common functions
----------------

.. automodule:: erpblok.client.common

.. autofunction:: list_databases
    :noindex:

.. autofunction:: create_database
    :noindex:

.. autofunction:: drop_database
    :noindex:

.. autofunction:: login_user
    :noindex:

.. autofunction:: logout
    :noindex:

.. autofunction:: format_static
    :noindex:

.. autofunction:: get_static
    :noindex:

.. autofunction:: get_templates_from
    :noindex:

Template definition module
--------------------------

.. automodule:: erpblok.client.template

.. autoexception:: TemplateException
    :members:
    :noindex:
    :show-inheritance:
    :inherited-members:

.. autoclass:: Template
    :members:
    :noindex:
    :show-inheritance:
    :inherited-members:
