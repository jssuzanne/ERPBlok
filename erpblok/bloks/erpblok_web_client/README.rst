This blok is required by all ERPBlok application. This blok define the main
fonctionnality of the interface and the user notion.

Functional space
----------------

The functional space is reprented by:
* Menu or not
* action(s) with their view(s)

.. code-block:: html

    <record external_id="setting_space_user">
        <field name="label">User</field>
        <field name="icon">fi-results-demographics</field>
        <field name="description">Configure the users and access rules</field>
        <field name="category" external_id="setting_space_category" />
        <field name="menus">
            <record external_id="setting_menu_groups">
                <!-- define one menu for the ``Groups`` model -->
                <field name="label">Groups</field>
                <field name="action" external_id="action_group"/>
            </record>
            <record external_id="setting_menu_logins">
                <field name="label">Logins</field>
                <field name="action" external_id="action_login"/>
            </record>
            <record external_id="setting_menu_users">
                <field name="label">Users</field>
                <field name="action" external_id="action_user"/>
            </record>
        </field>
    </record>

Menu
----

Space have often menus, this menu call action, in the same page or in a dialog
box. 

The menu can be hierarchical.

.. code-block:: html

    <record external_id="setting_space_low_level">
        <field name="label">Low level</field>
        <field name="icon">fi-wrench</field>
        <field name="description">Configure all the low level data</field>
        <field name="category" external_id="setting_space_category" />
        <field name="menus">
            <record>
                <field name="label">Database structure</field>
                <field name="children">
                    <record>
                        <field name="label">Models</field>
                        <field name="action" external_id="action_db_model"/>
                    </record>
                    <record>
                        <field name="label">Fields</field>
                        <field name="action" external_id="action_db_field"/>
                    </record>
                    <record>
                        <field name="label">Columns</field>
                        <field name="action" external_id="action_db_column"/>
                    </record>
                    <record>
                        <field name="label">Relation Ships</field>
                        <field name="action" external_id="action_db_rs"/>
                    </record>
                </field>
            </record>
        </field>
    </record>


Action
------

Is attach at the space or a dialog box. The action can have one or more view(s).

.. code-block:: html

    <record external_id="action_group">
        <field name="label">Groups</field>
        <field name="model">Model.Access.Group</field>
        <field name="add_delete">0</field>
        <field name="add_new">0</field>
        <field name="add_edit">0</field>
        <field name="views">
            <record external_id="view_access_group_tree">
                <field name="selectable">1</field>
                <field name="mode">Model.UI.View.List</field>
                <field name="template">ERPBlokAccessGroupList</field>
            </record>
        </field>
    </record>

View
----

Actuality the existing are:

List
~~~~

 * Can be modifiable directly in the line or open another type of view
 * Can be multi header
 * On field can be display more than one time.
 * they are some beaviour to help to display UI with some condition

.. code-block:: html
    
    <template id="ERPBlokAccessUserList">
        <field name="first_name" />
        <field name="last_name" />
    </template>


Possible attribute:

+----------------------+------------------------------------------------------+
| Attribute            | description                                          |
+======================+======================================================+
| checkbox             | Boolean, if the checkbox is displayed or not         |
+----------------------+------------------------------------------------------+
| inline               | Boolean, if the data is modified in the same view    |
+----------------------+------------------------------------------------------+

Form
~~~~

 * Can n be modifiable directly
 * On field can be display more than one time.
 * they are some beaviour to help to display UI with some condition

.. code-block:: html

    <template id="ERPBlokAccessWebLoginForm">
        <div class="row">
            <div class="columns small-12 medium-9 large-6">
                <label for="login" />
                <field name="login" />
                <label for="password" />
                <field name="password"/>
            </div>
        </div>
    </template>

thumbnail
~~~~~~~~~

 * Can open another type of view
 * On field can be display more than one time.
 * they are some beaviour to help to display UI with some condition

.. code-block:: html

    <template id="AnyBlokSystemBlokThumbnails">
        <div class="row">
            <div class="columns">
                <h4><field name="name" class="primary"/></h4>
            </div>
        </div>
        <div class="row">
            <div class="columns large-7 medium-6">
                <field name="logo" type="Picture" file_name_field="name"></field>
                <call template="AnyBlokSystemBlokButton"/>
            </div>
            <div class="columns large-5 medium-6">
                <call template="AnyBlokSystemBlokState"/>
            </div>
        </div>
    </template>

helper
~~~~~~

You can use some feature for the definition of the view:

 * call: include another template, do not rewrite more than one time the same
   template.


Field
-----

Each field represent one column in the database. If a column is put two time, 
modify one, automaticly modify the 2nd one. 

Declaration of one field 

.. code-block:: html

    <field name="my_anyblok_field"/>


The existing field Type are:

 * String
 * Integer
 * Boolean
 * Float
 * Selection
 * Password
 * Text
 * Html
 * LargeBinary
 * Picture
 * Many2One
 * One2One:
 * Many2ManyChoices

General attributes for all fields:

+----------------------+------------------------------------------------------+
| Attribute            | description                                          |
+======================+======================================================+
| name                 | Name of the anyblok field to display                 |
+----------------------+------------------------------------------------------+
| type                 | Type of field, by default, it is the AnyBlok field   |
+----------------------+------------------------------------------------------+
| writable-only-if     | take a condition::                                   |
|                      |                                                      |
|                      |    <field name="..."                                 |
|                      |           writable-only-if="fields.field1 != 'foo'"/>|
|                      |                                                      |
+----------------------+------------------------------------------------------+
| visible-only-if      | take a condition::                                   | 
|                      |                                                      |
|                      |    <field name="..."                                 |
|                      |           visible-only-if="fields.field1 != 'foo'"/> |
|                      |                                                      |
+----------------------+------------------------------------------------------+
| not-nullable-only-if | take a condition::                                   |
|                      |                                                      |
|                      |    <field name="..."                                 |
|                      |           not-nullable-only-if="fields.field1" />    |
|                      |                                                      |
+----------------------+------------------------------------------------------+



| placeholder |
| selections | 
| precision |

Attributes for field: LargeBinary

+----------------------+------------------------------------------------------+
| Attribute            | description                                          |
+======================+======================================================+
| file_name_field      | Name of the field to use to save the file name       |
+----------------------+------------------------------------------------------+
| file_size_field      | Name of the field to use to save the file size       |
+----------------------+------------------------------------------------------+
| mimetype_field       | Name of the field to use to save the file mimetype   |
+----------------------+------------------------------------------------------+
| accept               | filtering the extension of the file in the upload box|
+----------------------+------------------------------------------------------+

Attributes for field: Many2One

+----------------------+------------------------------------------------------+
| Attribute            | description                                          |
+======================+======================================================+
| search-box-limit     | Number max entry in the search select box            |
+----------------------+------------------------------------------------------+
| search-box-add       | Boolean to determine if the user can create a new    |
|                      | entry                                                |
+----------------------+------------------------------------------------------+
| label                | field of the relationship to use to display          |
+----------------------+------------------------------------------------------+

Attributes for field: Many2ManyChoices

+----------------------+------------------------------------------------------+
| Attribute            | description                                          |
+======================+======================================================+
| largegrid            | Number entry by line for large screen                | 
+----------------------+------------------------------------------------------+
| mediumgrid           | Number entry by line for tablette                    |
+----------------------+------------------------------------------------------+
| smallgrid            | Number entry by line for smartphone                  |
+----------------------+------------------------------------------------------+
| label                | field of the relationship to use to display          |
+----------------------+------------------------------------------------------+

Attributes for field: Text

+----------------------+------------------------------------------------------+
| Attribute            | description                                          |
+======================+======================================================+
| rows                 | Default rows number to display                       |
+----------------------+------------------------------------------------------+
