.. image:: https://readthedocs.org/projects/sfm/badge/?version=latest
    :target: https://sfm.readthedocs.io/index.html
    :alt: Documentation Status

.. image:: https://travis-ci.org/MacHu-GWU/single_file_module-project.svg?branch=master
    :target: https://travis-ci.org/MacHu-GWU/single_file_module-project?branch=master

.. image:: https://codecov.io/gh/MacHu-GWU/single_file_module-project/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/MacHu-GWU/single_file_module-project

.. image:: https://img.shields.io/pypi/v/sfm.svg
    :target: https://pypi.python.org/pypi/sfm

.. image:: https://img.shields.io/pypi/l/sfm.svg
    :target: https://pypi.python.org/pypi/sfm

.. image:: https://img.shields.io/pypi/pyversions/sfm.svg
    :target: https://pypi.python.org/pypi/sfm

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/single_file_module-project

------


.. image:: https://img.shields.io/badge/Link-Document-blue.svg
      :target: https://sfm.readthedocs.io/index.html

.. image:: https://img.shields.io/badge/Link-API-blue.svg
      :target: https://sfm.readthedocs.io/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Source_Code-blue.svg
      :target: https://sfm.readthedocs.io/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
      :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
      :target: https://github.com/MacHu-GWU/single_file_module-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
      :target: https://github.com/MacHu-GWU/single_file_module-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
      :target: https://github.com/MacHu-GWU/single_file_module-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
      :target: https://pypi.org/pypi/sfm#files


Welcome to ``sfm`` Documentation
==============================================================================

Collection of useful single file module. Please install required package respectively when needed.


winzip module
------------------------------------------------------------------------------
Suppose this is your file structure:

.. code-block:: bash

    /alice ($HOME)
        /Document
            /word
                /paper1.doc
                /paper2.doc
            /excel
                /data1.xlsx
                /data2.xlsx
            /readme.txt

Usage:

.. code-block:: python

    >>> from sfm.winzip import zip_a_folder, zip_everything_in_a_folder, zip_many_files
    >>> zip_a_folder("/Users/alice/Document", "/Users/alice/document.zip")
    >>> zip_everything_in_a_folder("/Users/alice/Document", "/Users/alice/document.zip")
    >>> zip_many_files(
        [
            "/Users/alice/Document/word/paper1.doc",
            "/Users/alice/Document/excel/data1.xlsx",
            "/Users/alice/Document/readme.txt",
        ],
        "/Users/alice/document.zip"
    )
    

timer module
------------------------------------------------------------------------------
Usage:

.. code-block:: python

    >>> import time
    >>> from sfm.timer import DateTimeTimer

    >>> with DateTimeTimer(title="first measure") as timer:
    ...     time.sleep(1)
    from xxxx-xx-xx xx:xx:xx.xxx to xxxx-xx-xx xx:xx:xx.xxx elapsed 1.000000 second.

    >>> timer = DateTimeTimer(title="second measure")
    >>> timer.start()
    >>> time.sleep(1)
    >>> timer.end()
    from xxxx-xx-xx xx:xx:xx.xxx to xxxx-xx-xx xx:xx:xx.xxx elapsed 1.000000 second.


And a lot more!


.. _install:

Install
-------------------------------------------------------------------------------

``sfm`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install sfm

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade sfm
