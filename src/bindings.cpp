#include <pybind11/pybind11.h>
#include "../algorithms/CubicalRipser_2dim/src/cubicalripser_2dim.h"
#include "Filter.h"
#include "Graph2D.h"
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
		  .def("filterBinaryL1", &Filter2D::filterBinaryL1)
		  .def("filterBinaryL2", &Filter2D::filterBinaryL2)
		  .def("filterBinaryLinf", &Filter2D::filterBinaryLinf)
		  //	Save filtration
		  .def("saveBinaryFiltration", &Filter2D::saveBinaryFiltration)
  	  	  .def("filter3StateAsBinary", &Filter2D::filter3StateAsBinary)  
		  ;
  
  py::class_<Vertex>(m, "Vertex")
		  .def(py::init<int, int, int>())
		  .def_readwrite("x", &Vertex::x)
		  .def_readwrite("y", &Vertex::y)
		  .def_readwrite("name", &Vertex::name)
		  ;
  
  py::class_<Graph2D>(m, "Graph2D")
		  .def(py::init<>())
		  .def("loadBinaryFromFile", &Graph2D::loadBinaryFromFile)
		  .def("generateGraph", &Graph2D::generateGraph)
		  .def("findLeafNodes", &Graph2D::findLeafNodes)
		  .def("addEdge", &Graph2D::addEdge)
		  .def("getEdge", &Graph2D::getEdge)
		  .def("getEdges", &Graph2D::getEdges)
		  .def("getVertex", &Graph2D::getVertex)
		  .def("getVertices", &Graph2D::getVertices)
		  ;
}  

