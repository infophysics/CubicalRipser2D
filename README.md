[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1467819.svg)](https://doi.org/10.5281/zenodo.1467819)


# CubicalRipser2D : Calculator of Persistent Homology of 2D Cubical Toplexes
 
 Copyright by Takeki Sudo and Kazushi Ahara, Meiji University, 2018
 (python bindings and modifications by Nicholas Carrara 2018)
 
 The following is a modified version of the original software written by T. Sudo and K. Ahara, which can be found here; https://github.com/CubicalRipser/CubicalRipser_2dim
 
 ## Installing from source
 
Requirements: You must have CMake>=2.8.12 and a C++11 compatible compiler (GCC>=4.8) to build.
  git clone https://github.com/infophysics/CubicalRipser2D.git
  cd CubicalRipser2D
  sudo python3 setup.py install
```
## Implementation
 ```python
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
 filt.filterBinaryVonNeumann(10)
 filt.saveBinaryFiltration("square2.csv")
 
 #    create CubicalRipser2D object
 cube2D = CubicalRipser2D()
 
 #    convert the filtration to DIPHA format
 convert_csv_to_dipha("square2.csv", "square_dipha.csv")
 
 #    compute the barcode and plot the persistence diagram
 cube2D.ComputeBarcode("square_dipha.csv", "test.csv", "DIPHA", "LINKFIND", 10, True)
 barcode = cube2D.getBarcode()
 plot_persistence_diagram(barcode)
 ```
 
 For more examples on possible calls, please see the Jupyter Notebook example.
 
 
 
 ### Support
 
 * Bugs: Please report bugs to the [issue tracker on Github](https://github.com/infophysics/CubicalRipser2D/issues) such that we can keep track of them and eventually fix them.  Please explain how to reproduce the issue (including code) and which system you are running on.
 * Help: Help can be provided also via the issue tracker by tagging your issue with 'question'
 * Contributing:  Please fork this repository then make a pull request.  In this pull request, explain the details of your change and include tests.
 
 ## Technical implementation
 
 This package is a [pybind11](https://pybind11.readthedocs.io/en/stable/intro.html) wrapper of several persistent homology algorithm implementations as well as general purpose plotting and a computation of the [Persistent Homology Dimension](https://people.math.osu.edu/schweinhart.2/MeasuringShapeWithTopology.pdf) (written by M. Tallon)
 
 * Help from Chris Tunnel, which included a great [binding tutorial](https://indico.cern.ch/event/694818/contributions/2985778/attachments/1682465/2703470/PyHEPTalk.pdf)
 * Implementation also based on [this](http://www.benjack.io/2018/02/02/python-cpp-revisited.html)
 
 See AUTHORS.md for information on the developers.
 
 ## Citation
 
 When you use `CubicalRipser2D`, please say so in your slides or publications (for publications, see Zenodo link above).  You can mention this in addition to how you cite CubicalRipser2D.  This is important for us being able to get funding to support this project.
