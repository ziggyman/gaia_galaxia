#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "../cpp/csvData.h"

namespace py = pybind11;

PYBIND11_MODULE(csvData2, m) {
    m.doc() = "pybind11 csvData2 plugin"; // optional module docstring

    py::class_<CSVData>(m, "CSVData")
        .def(py::init<>())
        .def_readwrite("header", &CSVData::header)
        .def_readwrite("data", &CSVData::data)
        .def("findKeywordPos", (int (CSVData::*)(string const&) const) &CSVData::findKeywordPos)
        .def("getData", (vector<string> (CSVData::*)(unsigned) const) &CSVData::getData)
        .def("getData", (vector<vector< string > > (CSVData::*)(vector<unsigned> const&) const) &CSVData::getData)
        .def("getData", (vector<string> (CSVData::*)(unsigned)) &CSVData::getData)
        .def("getData", (string (CSVData::*)(string const&, unsigned) const) &CSVData::getData)
        .def("getData", (vector<string> (CSVData::*)(string const&, vector<unsigned> const&) const) &CSVData::getData)
        .def("getData", (vector<string> (CSVData::*)(string const&) const) &CSVData::getData)
        .def("setData", (void (CSVData::*)(vector< vector< string > > &)) &CSVData::setData)
        .def("setData", (void (CSVData::*)(string const&, unsigned, string const&)) &CSVData::setData)
        .def("addColumn", (void (CSVData::*)(string const&, vector< string > const&)) &CSVData::addColumn)
        .def("addColumn", (void (CSVData::*)(string const&, vector< double > const&)) &CSVData::addColumn)
        .def("addColumn", (void (CSVData::*)(string const&)) &CSVData::addColumn)
        .def("removeColumn", (void (CSVData::*)(string const&)) &CSVData::removeColumn)
        .def("removeRow", (void (CSVData::*)(unsigned)) &CSVData::removeRow)
        .def("renameColumn", (void (CSVData::*)(string const&, string const&)) &CSVData::renameColumn)
        .def("size", (int (CSVData::*)() const) &CSVData::size)
        .def("append", (void (CSVData::*)(vector< string > const&)) &CSVData::append)
        .def("append", (void (CSVData::*)(vector< vector< string > > const&)) &CSVData::append)
        .def("append", (void (CSVData::*)(CSVData const&)) &CSVData::append)
        .def("find", (vector<int> (CSVData::*)(string const&, string const&) const) &CSVData::find)
        .def("find", (vector<int> (CSVData::*)(string const&, string const&, long) const) &CSVData::find)
        .def("findMultipleEntries", (std::pair< vector< string >, vector< vector< unsigned > > > (CSVData::*)(string const&) const) &CSVData::findMultipleEntries)
        .def("combineMultipleEntries", (void (CSVData::*)(string const&, vector<string> const&) const) &CSVData::combineMultipleEntries)
        .def("sort", (void (CSVData::*)(vector<unsigned> const&)) &CSVData::sort)
    ;

//    m.def("readHeader", (vector<string> (*)(string const&)) &readHeader);
//    m.def("readCSVFile", (CSVData (*)(string const&)) &readCSVFile);
//    m.def("convertStringVectortoDoubleVector", (vector<double> (*)(vector<string> const&)) &convertStringVectortoDoubleVector);
}
