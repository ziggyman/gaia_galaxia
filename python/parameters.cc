#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "../cpp/parameters.h"

namespace py = pybind11;

PYBIND11_MODULE(parameters, m) {
    m.doc() = "pybind11 parameters plugin"; // optional module docstring

    m.def("modelGetFileNameOutRoot", &modelGetFileNameOutRoot);
    m.def("gaiaGetFileNameOutRoot", &gaiaGetFileNameOutRoot);
    m.def("gaiaTgasGetFileNameOutRoot", &gaiaTgasGetFileNameOutRoot);
    m.def("modelGetDataDirOut", &modelGetDataDirOut);
    m.def("gaiaGetDataDirOut", &gaiaGetDataDirOut);
    m.def("gaiaTgasGetDataDirOut", &gaiaTgasGetDataDirOut);

}
