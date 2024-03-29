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
        .def(py::init<double, double, double, double>())
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

    py::class_<LonLat>(m, "LonLat")
        .def(py::init<>())
        .def(py::init<double, double>())
        .def_readwrite("lon", &LonLat::lon)
        .def_readwrite("lat", &LonLat::lat)
        .def("__repr__",
            [](const LonLat &a) {
                return "lon='" + to_string(a.lon)
                        + "', lat='" + to_string(a.lat) + "'";
            })
    ;

    py::class_<Hammer>(m, "Hammer")
        .def(py::init<>())
        .def("isInside", (bool (Hammer::*)(double, double) const) &Hammer::isInside)
        .def("isInside", (bool (Hammer::*)(const XY &) const) &Hammer::isInside)
        .def("isInside", (bool (Hammer::*)(const Pixel &, const double, const double) const) &Hammer::isInside)
        .def("isInside", (bool (Hammer::*)(const Pixel &, const XY &) const) &Hammer::isInside)
        .def("getPixelContaining", (Pixel (Hammer::*)(XY const xy) const) &Hammer::getPixelContaining)
        .def("getPixelContaining", (Pixel (Hammer::*)(XY const xy, bool const smallerPixelsTowardsCenter) const) &Hammer::getPixelContaining)
        .def("getPixels", (vector< Pixel > (Hammer::*)() const) &Hammer::getPixels)
        .def("getPixelsSmallTowardsCenter", (vector< Pixel > (Hammer::*)() const) &Hammer::getPixelsSmallTowardsCenter)
        .def("lonLatToXY", (XY (Hammer::*)(const double &, const double &) const) &Hammer::lonLatToXY)
        .def("lonLatToXY", (vector< vector< double > > (Hammer::*)(vector<double> &, vector<double> &) const) &Hammer::lonLatToXY)
        .def("xYToLonLat", (LonLat (Hammer::*)(const double &, const double &) const) &Hammer::xYToLonLat)
        .def("getKeyWordHammerX", (string (Hammer::*)() const) &Hammer::getKeyWordHammerX)
        .def("getKeyWordHammerY", (string (Hammer::*)() const) &Hammer::getKeyWordHammerY)
//        .def("plotGrid", (bool (Hammer::*)(string)) &Hammer::plotGrid)
    ;
}
