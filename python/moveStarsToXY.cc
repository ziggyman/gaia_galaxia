#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "../cpp/moveStarsToXY.h"

namespace py = pybind11;

PYBIND11_MODULE(moveStarsToXY, m) {
    m.def("getOutFiles", &getOutFiles);
    m.def("getOutFileNames", &getOutFileNames);
    m.def("writeHeaderToOutFiles", &writeHeaderToOutFiles);
    m.def("appendCSVDataToXYFiles", &appendCSVDataToXYFiles);
}
