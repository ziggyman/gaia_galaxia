#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "../cpp/galcomp.h"

namespace py = pybind11;

PYBIND11_MODULE(galcomp, m) {
    m.doc() = "pybind11 galcomp plugin"; // optional module docstring

    m.def("countStars", &countStars);
}
