==============
kotti2_tinymce
==============

TinyMCE plugins for Kotti2.

.. image:: https://img.shields.io/pypi/v/kotti2_tinymce.svg?style=flat-square
    :target: https://pypi.org/project/kotti2_tinymce/
    :alt: PyPI Version

Setup
=====

Install the package::

    pip install kotti2_tinymce

To activate the kotti_tinymce add-on in your Kotti2 site, you need to
add an entry to the ``kotti.configurators`` setting in your Paste
Deploy config.  If you don't have a ``kotti.configurators`` option,
add one.  The line in your ``[app:main]`` section could then look like
this::

  kotti.configurators = kotti_tinymce.kotti_configure

With this, you'll be able to use TinyMCE in your Kotti2 site.

`Find out more about Kotti2`_

.. _Find out more about Kotti2: https://pypi.org/project/Kotti2/
