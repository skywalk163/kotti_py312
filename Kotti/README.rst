======
Kotti2
======

.. image:: https://img.shields.io/pypi/v/Kotti2.svg?style=flat-square
    :target: https://pypi.org/project/Kotti2/
    :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/Kotti2.svg?style=flat-square
    :target: https://pypi.org/project/Kotti2/
    :alt: Python Versions

.. image:: https://img.shields.io/pypi/l/Kotti2.svg?style=flat-square
    :target: http://www.repoze.org/LICENSE.txt
    :alt: License

.. image:: https://github.com/skywalk163/kotti_py312/actions/workflows/sqlite.yml/badge.svg
    :target: https://github.com/skywalk163/kotti_py312/actions/workflows/sqlite.yml
    :alt: SQLite Tests

.. image:: https://github.com/skywalk163/kotti_py312/actions/workflows/postgres.yml/badge.svg
    :target: https://github.com/skywalk163/kotti_py312/actions/workflows/postgres.yml
    :alt: PostgreSQL Tests

.. image:: https://github.com/skywalk163/kotti_py312/actions/workflows/mysql.yml/badge.svg
    :target: https://github.com/skywalk163/kotti_py312/actions/workflows/mysql.yml
    :alt: MySQL Tests

**Kotti2** is a fork of Kotti CMS with Python 3.12 and SQLAlchemy 2.0 support.

Kotti is a high-level, Pythonic web application framework based on Pyramid_ and SQLAlchemy_.
It includes an extensible Content Management System called the Kotti CMS (see below).

Kotti is most useful when you are developing applications that

- have complex security requirements,
- use workflows, and/or
- work with hierarchical data.

Built on top of a number of *best-of-breed* software components,
most notably Pyramid_ and SQLAlchemy_,
Kotti introduces only a few concepts of its own,
thus hopefully keeping the learning curve flat for the developer.


.. _Pyramid: http://docs.pylonsproject.org/projects/pyramid/dev/
.. _SQLAlchemy: http://www.sqlalchemy.org/

Kotti CMS
=========

Kotti CMS is a content management system that's heavily inspired by Plone_.
Its **main features** are:

- **User-friendliness**: editors can edit content where it appears;
  thus the edit interface is contextual and intuitive

- **WYSIWYG editor**: includes a rich text editor

- **Responsive design**: Kotti builds on `Bootstrap`_, which
  looks good both on desktop and mobile

- **Templating**: you can extend the CMS with your own look & feel
  with almost no programming required

- **Add-ons**: install a variety of add-ons and customize them as well
  as many aspects of the built-in CMS by use of an INI configuration
  file

- **Security**: the advanced user and permissions management is
  intuitive and scales to fit the requirements of large organizations

- **Internationalized**: the user interface is fully translatable,
  Unicode is used everywhere to store data

.. _Plone: http://plone.org/
.. _Bootstrap: http://getbootstrap.com/

What's Different from Kotti
===========================

Kotti2 is a fork that includes:

- **Python 3.12 support**: Full compatibility with Python 3.12
- **SQLAlchemy 2.0 support**: Updated to work with SQLAlchemy 2.0.49
- **Test coverage**: 379/379 tests passing (100%)

Security Advisory
=================

.. warning::

   **Beaker Session Vulnerability (CVE-2013-7489)**
   
   The default session factory uses Beaker, which has a known `pickle deserialization 
   vulnerability <https://nvd.nist.gov/vuln/detail/CVE-2013-7489>`_ that could lead to 
   remote code execution. This vulnerability exists when untrusted data is deserialized.

**Recommended Action:**

If your application doesn't store large amounts of data in sessions (cookie limit is ~4KB), 
switch to the secure cookie-based session factory by adding this to your INI configuration::

    kotti.session_factory = kotti.signed_cookie_session_factory

**Why Beaker is Still the Default:**

- Cookie-based sessions have a ~4KB size limit
- Some applications store large data in sessions (e.g., file uploads, clipboard operations)
- Beaker supports server-side storage (file, database, memcached) without size limits

**Migration Guide:**

1. **For simple applications** (small session data):
   
   Change your INI file::
   
       kotti.session_factory = kotti.signed_cookie_session_factory
       
   Optional configuration::
   
       kotti.session.timeout = 3600
       kotti.session.secure = true
       kotti.session.httponly = true

2. **For applications with large session data**:
   
   Continue using Beaker but configure server-side storage::
   
       session.type = file
       session.data_dir = /path/to/sessions/data
       session.lock_dir = /path/to/sessions/lock
   
   Or use database-backed sessions for better security.

License
=======

Kotti2 is offered under the BSD-derived `Repoze Public License <http://repoze.org/license.html>`_.

Install
=======

::

    pip install Kotti2

Available Plugins
==================

- **kotti2_image**: Image content type with thumbnail support
- **kotti2_tinymce**: TinyMCE rich text editor integration
- **kotti2_g4f**: GPT4Free AI chat integration

::

    pip install kotti2_image kotti2_tinymce kotti2_g4f

Support and Documentation
=========================

Read the original `Kotti documentation <https://kotti.readthedocs.io/>`_ on `Read the Docs <https://readthedocs.org/>`_.

Development
===========

Kotti2 is actively maintained with Python 3.12 and SQLAlchemy 2.0 support.

Contributions are welcome!
