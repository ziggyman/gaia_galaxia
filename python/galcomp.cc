#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "../cpp/galcomp.h"
#include "../cpp/csvData.h"

namespace py = pybind11;

PYBIND11_MODULE(galcomp, m) {
    m.doc() = "pybind11 galcomp plugin"; // optional module docstring

    m.def("countStars", &countStars);
    m.def("getStarsInXYWindow", (CSVData (*)(vector<Pixel> const&, Pixel const&, string const&)) &getStarsInXYWindow);
    m.def("makeHistogram", (void (*)(vector<Pixel> const&,Pixel const&,vector<string> const&,string const&,vector< pair< float, float > >,string const&)) &makeHistogram);
}
