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
		.def(py::init<const char*, std::string, double>())
		.def(py::init<std::vector<std::vector<double> >, double>())
	  	.def("ComputeBarcode", (void (CubicalRipser2D::*)(const char*, string, string, double, bool)) &CubicalRipser2D::ComputeBarcode)
	  	.def("ComputeBarcode", (void (CubicalRipser2D::*)(const char*, string, double, bool)) &CubicalRipser2D::ComputeBarcode)
	  	.def("ComputeBarcode", (void (CubicalRipser2D::*)()) &CubicalRipser2D::ComputeBarcode)
		.def("getBarcode", &CubicalRipser2D::getBarcode)
		;

  py::class_<Filter2D>(m, "Filter2D")
		  .def(py::init<>())
		  .def(py::init<std::vector<std::vector<double> >>())
		  .def("loadBinaryFromFile", &Filter2D::loadBinaryFromFile)
		  //	Various filterings
		  //	Binary filterings
		  .def("filterBinaryL1", &Filter2D::filterBinaryL1)
		  .def("filterBinaryL2", &Filter2D::filterBinaryL2)
		  .def("filterBinaryLinf", &Filter2D::filterBinaryLinf)
		  //	Save filtration
		  .def("saveBinaryFiltration", &Filter2D::saveBinaryFiltration)
  	  	  .def("filter3StateAsBinary", &Filter2D::filter3StateAsBinary)  
		  .def("getBinaryFiltration", &Filter2D::getBinaryFiltration)
		  ;
}  

