#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "../cpp/csvData.h"

namespace py = pybind11;

PYBIND11_MODULE(csvData, m) {
    m.doc() = "pybind11 csvData plugin"; // optional module docstring

    py::class_<CSVData>(m, "CSVData")
        .def(py::init<>())
        .def_readwrite("header", &CSVData::header)
        .def_readwrite("data", &CSVData::data)
        .def("getData", (string (CSVData::*)(string const&, int) const) &CSVData::getData)
        .def("getData", (vector<string> (CSVData::*)(string const&) const) &CSVData::getData)
        .def("setData", (void (CSVData::*)(vector< vector< string > > &)) &CSVData::setData)
        .def("addColumn", (void (CSVData::*)(string const&, vector< string > const&)) &CSVData::addColumn)
        .def("addColumn", (void (CSVData::*)(string const&, vector< double > const&)) &CSVData::addColumn)
        .def("size", (int (CSVData::*)() const) &CSVData::size)
    ;

//    m.def("readHeader", (vector<string> (*)(string const&)) &readHeader);
//    m.def("readCSVFile", (CSVData (*)(string const&)) &readCSVFile);
//    m.def("convertStringVectortoDoubleVector", (vector<double> (*)(vector<string> const&)) &convertStringVectortoDoubleVector);
}
