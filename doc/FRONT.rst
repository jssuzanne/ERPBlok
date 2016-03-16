.. contents::

Front Matter
============

Information about the ERPBlok project.

Project Homepage
----------------

ERPBlok is hosted on `Bitbucket <http://bitbucket.org>`_ - the main project
page is at https://bitbucket.org/jssuzanne/erpblok. Source code is tracked here
using `Mercurial <http://mercurial.selenic.com>`_.

.. Releases and project status are available on Pypi at 
.. http://pypi.python.org/pypi/anyblok.

The most recent published version of this documentation should be at
http://docs.erpblok.fr/erpblok/default.

Project Status
--------------

AnyBlok is currently in dev status and is expected to be fairly
stable.   Users should take care to report bugs and missing features on an as-needed
basis.  It should be expected that the development version may be required
for proper implementation of recently repaired issues in between releases;
the latest master is always available at http://bitbucket/jssuzanne/erpblok/get/default.tar.gz.
or http://bitbucket.org/jssuzanne/erpblok/get/default.zip

Installation
------------

.. Install released versions of AnyBlok from the Python package index with 
.. `pip <http://pypi.python.org/pypi/pip>`_ or a similar tool::
.. 
..     pip install erpblok

Installation via source distribution is via the ``setup.py`` script::

    python setup.py install

Installation will add the ``AnyBlok`` and ``AnyBlok / Pyramid`` and ``gunicorn``
commands to the environment.

Unit Test
---------

Run the framework test with ``nose``::

    pip install nose
    nosetests erpblok/tests

Run all the installed bloks::

    anyblok_nose -c config.file.cfg

Run the blok tests at the installation::

    anyblok_updatedb -c config.file.cfg --install_bloks myblok --test-blok-at-install

AnyBlok are tested by the `Anybox <http://anybox.fr>`_ `builbot <http://buildbot.anyblok.org>`_

Dependencies
------------

AnyBlok works with **Python 3.2** and later. The install process will
ensure that `AnyBlok <http://doc.anyblok.org>`_,
`AnyBlok / Pyramid <http://docs.anybox.fr/anyblok_pyramid/default/>`_ are installed, in addition to
other dependencies. The latest version of them is strongly recommended.


Contributing (hackers needed!)
------------------------------

ERPblok is at a very early stage, feel free to fork, talk with core dev, and spread the word!

Author
------

Jean-Sébastien Suzanne

Contributors
------------

`Anybox <http://anybox.fr>`_ team:

* Jean-Sébastien Suzanne
* Pierre Verkest

Bugs
----

Bugs and feature enhancements to AnyBlok should be reported on the `Issue 
tracker <https://bitbucket.org/jssuzanne/erpblok/issues?status=new&status=open>`_.
