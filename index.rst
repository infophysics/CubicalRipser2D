.. cube2d documentation master file, created by
   sphinx-quickstart on Thu Nov  8 08:05:08 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


|PyPI version| |Travis-CI| |Appveyor| |Codecov| |License: MIT|


Cube2D.py
==================================

Cube2D.py is a persistent homologu package which computes persistence on two-dimensional cubical toplexes, and is a derivative of the RIPSER algorithm. This fast implementation consists of the following features, 

- computing persistence cohomology of digitized binary images,
- visualizing persistence diagrams, 
- filtering binary images according to L1, L2 and Linf distances,
- visualizing filtered binary images. 

Additionally, through extensive testing and continuous integration, Cube2D.py is easy to install on Mac, Linux, and Windows platforms.

We supply a large set of interactive notebooks that demonstrate how to take advantage of all the features available.

You can find the source code on github at `Scikit-TDA/Ripser.py <https://github.com/scikit-tda/Cube2D.py>`_. For the original C++ library, see `CubicalRipser/CubicalRipser_2dim/ <https://github.com/CubicalRipser/CubicalRipser_2dim/releases/latest>`_.

Example Usage
-------------


.. code:: python

    from Cube2D import CubicalRipser2D
    grid = [[1,1,1],[1,2,1],[1,1,1]]

    cube2d = CubicalRipser2D(grid, 10)
    cube2d.ComputeBarcode()
    Cube2D.plot_persistence_diagram(cube2d.getBarcode(), threshold=10)

.. toctree::
    :maxdepth: 2
    :caption: Background

    about
    Basic Usage

.. toctree::
    :maxdepth: 2
    :caption: Tutorials

.. toctree::
    :maxdepth: 2
    :caption: API Reference
    
    reference


.. |PyPI version| image:: https://badge.fury.io/py/ripser.svg
   :target: https://badge.fury.io/py/ripser

.. |Travis-CI| image:: https://travis-ci.org/scikit-tda/ripser.py.svg?branch=master
    :target: https://travis-ci.org/scikit-tda/ripser.py

.. |Appveyor| image:: https://ci.appveyor.com/api/projects/status/020nrvrq2rdg2iu1?svg=true
    :target: https://ci.appveyor.com/project/sauln/ripser-py

.. |Codecov| image:: https://codecov.io/gh/scikit-tda/ripser.py/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/scikit-tda/ripser.py

.. |License: MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT)

