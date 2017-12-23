#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "../cpp/galcomp.h"

namespace py = pybind11;

PYBIND11_MODULE(galcomp, m) {
    m.doc() = "pybind11 galcomp plugin"; // optional module docstring

//    m.def("add", &add, "A function which adds two numbers");
//    py::class_<Pet>(m, "Pet")
//        .def(py::init<const std::string &>())
//        .def("setName", &Pet::setName)
//        .def("getName", &Pet::getName);

//    a free function:
//    m.def("get_data", &get_data, return_value_policy::reference);

    py::class_<CSVData>(m, "CSVData")
        .def(py::init<>())
        .def_readwrite("header", &CSVData::header)
        .def_readwrite("data", &CSVData::data)
        .def("getData", (string (CSVData::*)(string const&, int) const) &CSVData::getData)
        .def("getData", (vector<string> (CSVData::*)(string const&) const) &CSVData::getData)
        .def("setData", (void (CSVData::*)(vector< vector< string > > &)) &CSVData::setData)
        .def("size", (int (CSVData::*)() const) &CSVData::size)
//        .def("setDataSize", (bool (CSVData::*)(int, int)) &CSVData::setDataSize)
    ;


//    py::class_<Hammer>(m, "Hammer")
//        .def(py::init<>())
//        .def("isInside", (bool (Hammer::*)(double, double)) &Hammer::isInside)
//        .def("isInside", (bool (Hammer::*)(const XY &)) &Hammer::isInside)
//        .def("getPixels", &Hammer::getPixels)
//        .def("lonLatToXY", (XY (Hammer::*)(const double &, const double &) const) &Hammer::lonLatToXY)
//        .def("lonLatToXY", (vector< vector< double > > (Hammer::*)(vector<double> &, vector<double> &) const) &Hammer::lonLatToXY)
//    ;
}
