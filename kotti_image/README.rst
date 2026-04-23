kotti2_image
************

This is an extension to Kotti2 that allows you to add images to your site.

**This package is only compatible with Kotti2 version 3.0.0 and later.**

.. image:: https://img.shields.io/pypi/v/kotti2_image.svg?style=flat-square
    :target: https://pypi.org/project/kotti2_image/
    :alt: PyPI Version

.. image:: https://img.shields.io/pypi/l/kotti2_image.svg?style=flat-square
    :target: http://www.repoze.org/LICENSE.txt
    :alt: License

`Find out more about Kotti2`_

.. _Find out more about Kotti2: https://pypi.org/project/Kotti2/

Setup
=====

To enable the extension in your Kotti2 site::

    pip install kotti2_image

Then activate the configurator in your INI file::

    kotti.configurators =
        kotti_image.kotti_configure

Configuration
=============

The initial release doesn't provide any configuration options.
Custom configuration of image scales will be available in future releases.

Upgrading
=========

If you are upgrading from a previous version you might have to migrate your database.
The migration is performed with `alembic`_ and Kotti's console script ``kotti-migrate``.
To migrate, run ``kotti-migrate <your.ini> upgrade --scripts=kotti_image:alembic`` (or ``kotti-migrate <your.ini> upgrade_all`` to run all Kotti and add on migrations).

For integration of alembic in your environment please refer to the `alembic documentation`_.

Development
===========

Contributions to kotti2_image are highly welcome.

.. _alembic: http://pypi.python.org/pypi/alembic
.. _alembic documentation: http://alembic.readthedocs.org/en/latest/index.html
