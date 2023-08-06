===========
pop-archive
===========

.. image:: https://img.shields.io/badge/made%20with-pop-teal
   :alt: Made with pop, a Python implementation of Plugin Oriented Programming
   :target: https://pop.readthedocs.io/

.. image:: https://img.shields.io/badge/made%20with-python-yellow
   :alt: Made with Python
   :target: https://www.python.org/

POP archive function provider for TAR, ZIP, RAR, etc.

About
=====

This project is app-merged into other POP projects in order to provide archive
handling functionality. See the POP docs for more information on how that
happens.

What is POP?
------------

This project is built with `pop <https://pop.readthedocs.io/>`__, a Python-based
implementation of *Plugin Oriented Programming (POP)*. POP seeks to bring
together concepts and wisdom from the history of computing in new ways to solve
modern computing problems.

For more information:

* `Intro to Plugin Oriented Programming (POP) <https://pop-book.readthedocs.io/en/latest/>`__
* `pop-awesome <https://gitlab.com/saltstack/pop/pop-awesome>`__
* `pop-create <https://gitlab.com/saltstack/pop/pop-create/>`__

Getting Started
===============

Prerequisites
-------------

* Python 3.6+
* git *(if installing from source, or contributing to the project)*

Installation
------------

.. note::

   If wanting to contribute to the project, and setup your local development
   environment, see the ``CONTRIBUTING.rst`` document in the source repository
   for this project.

If wanting to use ``pop-archive``, you can do so by either
installing from PyPI or from source.

Install from PyPI
+++++++++++++++++

.. code-block:: bash

   pip install pop-archive

Install from source
+++++++++++++++++++

.. code-block:: bash

   # clone repo
   git clone git@<your-project-path>/pop-archive.git
   cd pop-archive

   # Setup venv
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e .

Acknowledgements
================

* `Img Shields <https://shields.io>`__ for making repository badges easy.
