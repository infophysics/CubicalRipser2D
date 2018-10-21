#include <pybind11/pybind11.h>
#include "../algorithms/CubicalRipser_2dim/src/cubicalripser_2dim.h"
#include "Filter.h"
#include <pybind11/stl_bind.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>


namespace py = pybind11;

PYBIND11_MODULE(cube2d, m) {
  //	Binding for CubicalRipser2D
  py::class_<CubicalRipser2D>(m, "CubicalRipser2D")
		.def(py::init<>())
	  	.def("ComputeBarcode", &CubicalRipser2D::ComputeBarcode)
		.def("getBarcode", &CubicalRipser2D::getBarcode)
		;
  
  py::class_<Filter2D>(m, "Filter2D")
		  .def(py::init<>())
		  .def("loadBinaryFromFile", &Filter2D::loadBinaryFromFile)
		  //	Various filterings
		  //	Binary filterings
		  .def("filterBinaryVonNeumann", &Filter2D::filterBinaryVonNeumann)
		  .def("filterBinaryMoore", &Filter2D::filterBinaryMoore)
		  //	Save filtration
		  .def("saveBinaryFiltration", &Filter2D::saveBinaryFiltration)
  	  	  .def("filter3StateAsBinary", &Filter2D::filter3StateAsBinary)  
		  ;
}  

