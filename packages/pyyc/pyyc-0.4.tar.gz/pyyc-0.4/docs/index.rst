pyYC documentation
##################

:Version: |version| of |today|
:Author: Yannick Copin <y.copin@ipnl.in2p3.fr>

:Abstract: This package should be used as a template for package
           structure, configuration and packaging, documentation,
           tests, gitlab continuous integration, etc. *Work In
           Progress*

.. highlight:: console

..
   PyPY does not support sphinx markup in top-level README. Keep it minimal,
   and add full description in documentation.

.. include:: ../README.rst
.. include:: readme.rst

.. toctree::
   :hidden:

   __main__
   setup
   gitlab-ci

Code documentation
==================

.. toctree::
   :caption: Packages and modules

   pyyc

.. toctree::
   :titlesonly:
   :caption: Main entries

   main

Notebooks
=========

.. toctree::
   :titlesonly:

   notebooks/pyyc.ipynb

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
