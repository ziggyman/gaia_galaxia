#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "../cpp/hammer.h"

namespace py = pybind11;

PYBIND11_MODULE(hammer, m) {
    m.doc() = "pybind11 hammer plugin"; // optional module docstring

//    m.def("add", &add, "A function which adds two numbers");
//    py::class_<Pet>(m, "Pet")
//        .def(py::init<const std::string &>())
//        .def("setName", &Pet::setName)
//        .def("getName", &Pet::getName);

//    a free function:
//    m.def("get_data", &get_data, return_value_policy::reference);

    py::class_<Pixel>(m, "Pixel")
        .def(py::init<>())
        .def("isInside", &Pixel::isInside)
        .def_readwrite("xLow", &Pixel::xLow)
        .def_readwrite("xHigh", &Pixel::xHigh)
        .def_readwrite("yLow", &Pixel::yLow)
        .def_readwrite("yHigh", &Pixel::yHigh)
        .def("__repr__",
            [](const Pixel &a) {
                return "xLow='" + to_string(a.xLow)
                        + "', xHigh='" + to_string(a.xHigh)
                        + "', yLow='" + to_string(a.yLow)
                        + "', yHigh='" + to_string(a.yHigh) + "'";
            })
    ;

    py::class_<XY>(m, "XY")
        .def(py::init<>())
        .def(py::init<double, double>())
        .def_readwrite("x", &XY::x)
        .def_readwrite("y", &XY::y)
        .def("__repr__",
            [](const XY &a) {
                return "x='" + to_string(a.x)
                        + "', y='" + to_string(a.y) + "'";
            })
    ;

    py::class_<Hammer>(m, "Hammer")
        .def(py::init<>())
        .def("isInside", (bool (Hammer::*)(double, double)) &Hammer::isInside)
        .def("isInside", (bool (Hammer::*)(const XY &)) &Hammer::isInside)
        .def("getPixels", &Hammer::getPixels)
        .def("lonLatToXY", (XY (Hammer::*)(const double &, const double &) const) &Hammer::lonLatToXY)
        .def("lonLatToXY", (vector< vector< double > > (Hammer::*)(vector<double> &, vector<double> &) const) &Hammer::lonLatToXY)
    ;
}
