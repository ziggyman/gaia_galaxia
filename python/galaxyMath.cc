#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <string>
#include "../cpp/galaxyMath.h"

namespace py = pybind11;

PYBIND11_MODULE(galaxyMath, m) {
    m.doc() = "pybind11 galaxyMath plugin"; // optional module docstring

    m.def("raDecToLB", (pair<double, double> (*)(double, double)) &raDecToLB);
    m.def("radToDeg", (double (*)(double)) &radToDeg);
    m.def("degToRad", (double (*)(double)) &degToRad);
    m.def("muRaDecToMuLB", (pair<double, double> (*)(double, double, double, double)) &muRaDecToMuLB);
    m.def("parallaxToDistance", (vector<double> (*)(vector<double> const&)) &parallaxToDistance);
    m.def("getICRSUnitVector", (vector<double> (*)(double const&, double const&)) &getICRSUnitVector);
    m.def("getGalUnitVector", (vector<double> (*)(double const&, double const&)) &getGalUnitVector);
}
