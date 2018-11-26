#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <string>
#include "../cpp/csvData.h"

namespace py = pybind11;

PYBIND11_MODULE(csvFree, m) {
    m.doc() = "pybind11 csvFree plugin"; // optional module docstring

    m.def("readHeader", (vector<string> (*)(string const&)) &readHeader);
    m.def("countCharPerLine", (vector<int> (*)(string const&, char const&)) &countCharPerLine);
    m.def("readCSVFile", (CSVData (*)(string const&, bool const&)) &readCSVFile);
    m.def("readCSVFile", (CSVData (*)(string const&)) &readCSVFile);
    m.def("convertStringVectorToDoubleVector", (vector<double> (*)(vector<std::string> const&)) &convertStringVectorToDoubleVector);
    m.def("convertStringVectorToUnsignedVector", (vector<unsigned> (*)(vector<std::string> const&)) &convertStringVectorToUnsignedVector);
    m.def("convertDoubleVectorToStringVector", (vector<std::string> (*)(vector<double> const&)) &convertDoubleVectorToStringVector);
    m.def("appendFile", (void (*)(string const&, string const&)) &appendFile);
}
