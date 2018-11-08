About
======


Cube2D.py is an evolution of the original C++ Ripser project and the CubicalRipser C++ project.   We have put extensive work into making the package available to Python developers across all major platforms. If you are having trouble installing, please let us know by opening a github issue.


Setup
------

Cube2D.py is not yet available on Pypi, however we hope to have it there soon. To install, you'll first need the python version of cmake, 

.. code:: python

    pip install cmake

Then, clone the repository from github,

.. code:: python
    
    git clone https://github.com/infophysics/CubicalRipser2D.git

This distribution was built using pybind11, which is included in the distribution.  To build simply run the setup.py file

.. code:: python

    cd CubicalRipser2D
    python setup.py install

 
Usage
------

.. code:: python

    import Cube2D
    from Cube2D import CubicalRipser2D, Filter2D

    #    create a 5x5 grid with the homology of S^1
    grid = [[1,1,1,1,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,1]]

    #    write this data to file
    with open("square.csv", 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerows(grid)
    
    #   try 2D von neumann filter
    filt = Filter2D()
    filt.loadBinaryFromFile("square.csv")
    filt.filterBinaryL1(10)
    filt.saveBinaryFiltration("square2.csv")

    #    create CubicalRipser2D object
    cube2D = CubicalRipser2D()

    #    convert the filtration to DIPHA format
    convert_csv_to_dipha("square2.csv", "square_dipha.csv")

    #    compute the barcode and plot the persistence diagram
    cube2D.ComputeBarcode("square_dipha.csv", "test.csv", "DIPHA", 10, True)
    barcode = cube2D.getBarcode()
    plot_persistence_diagram(barcode)


License
--------

Cube2D.py is available under an LGPL license! The core C++ code is derived from CubicalRipser_2dim, which is also available under an LGPL license and copyright to T. Sudo and K. Ahara.  The modifications, Python code, and documentation is copyright to Nicholas Carrara.

