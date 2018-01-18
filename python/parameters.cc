#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "../cpp/parameters.h"

namespace py = pybind11;

PYBIND11_MODULE(parameters, m) {
    m.doc() = "pybind11 parameters plugin"; // optional module docstring

    m.def("galaxiaGetFileNameOutRoot", &galaxiaGetFileNameOutRoot);
    m.def("gaiaGetFileNameOutRoot", &gaiaGetFileNameOutRoot);
    m.def("gaiaTgasGetFileNameOutRoot", &gaiaTgasGetFileNameOutRoot);
    m.def("galaxiaGetDataDirOut", &galaxiaGetDataDirOut);
    m.def("gaiaGetDataDirOut", &gaiaGetDataDirOut);
    m.def("gaiaTgasGetDataDirOut", &gaiaTgasGetDataDirOut);

}
