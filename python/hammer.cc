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
    py::class_<Pixel>(m, "Pixel")
        .def(py::init<>())
        .def("isInside", &Pixel::isInside);
    py::class_<XY>(m, "XY")
        .def(py::init<>())
        .def(py::init<double, double>());
    py::class_<Hammer>(m, "Hammer")
        .def(py::init<>())
        .def("isInside", (bool (Hammer::*)(double, double)) &Hammer::isInside)
        .def("isInside", (bool (Hammer::*)(const XY &)) &Hammer::isInside)
        .def("getPixels", &Hammer::getPixels);
}
