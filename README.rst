`secualert` Sphinx Extension
============================

This package contains the `secualert` `Sphinx`_ extension.

:project: `sphinxcontrib-secualert`
:version: 0.1
:authors: Vincent Férotin, Sphinx team
:license: BSD 2-Clause License (see `LICENSE` file)

This extension was created to specifically list as security alerts
items previously targeted as `todo`, and allow listing all alerts
in one list, different from `todolist`.
It was developped from a copy of :mod:`sphinx.ext.todo`.


Usage
-----

Extension need to be installed aside Sphinx, from sources:

.. code-block:: sh

    # in extension sources root directory
    # with Sphinx virtualenv activated if any
    $ pip install .

and then activated in project's documentation configuration;

.. code-block:: py
    :name: doc/conf.py

    # ...
    extensions = [
        # ...
        'sphinxcontrib.secualert',
    ]
    # ...

This extension introduces two new directives:

*   ``.. secualert::`` for creating a new security-related alert item;
*   ``.. secualertlist::`` for re-listing in one place all security-related
    alerts items.

Intended usage is same as :mod:`sphinx.ext.todo` extension:

.. code-block:: rst

    .. secualert:: This is a basic security alert item!

    .. List all alerts:

    .. secualertlist::


.. _Sphinx: http://www.sphinx-doc.org/

