Description
===========
    Doyle is project to build the automation tool for date exploration and data preprocessing as a python package. 
    Doyle is in initial process so the package and documents are not complete for now.

Installation
============
    In current version, Doyle only support for python 3.7

.. code-block:: bash
    pip install doyle
    # then, install sherlock package with the following command
    pip install -e git+https://github.com/mitmedialab/sherlock-project.git#egg=sherlock

Documents
============
    the documents are not available for now

Usage
=====
.. code-block:: bash
    >>> import doyle
    >>> explorer = doyle.DataExplorer.explore_files("./data")
