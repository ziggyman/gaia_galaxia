#ifndef __CSVDATA_H__
#define __CSVDATA_H__

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <sys/time.h>
#include <vector>

#include "galaxyMath.h"
#include "parameters.h"

using namespace std;

struct CSVData{
    vector<string> header;
    vector< vector< string > > data;

    int findKeywordPos(string const& keyword) const;

    vector<string> getData(unsigned row) const;

    vector<string> getData(unsigned row);

    vector< vector< string > > getData(vector<unsigned> const& rows) const;

    vector< vector< string > > getData(vector<int> const& rows) const;

    string getData(string const& keyword, unsigned row) const;

    vector<string> getData(string const& keyword) const;

    vector<string> getData(string const& keyword, vector<unsigned> const& rows) const;

    vector<string> getData(string const& keyword, vector<int> const& rows) const;

    void setData(vector< vector< string > > & dataIn);

    void setData(string const& keyword, unsigned row, string const& value);

    void addColumn(string const& colName, vector<string> const& colData);

    void addColumn(string const& colName);

    void addColumn(string const& colName, vector<double> const& colData);

    int size() const;

    void append(vector<string> const& newLine);

    void append(vector< vector< string > > const& newLines);

    void append(CSVData const& csv);

    void removeRow(unsigned row);

    /// find multiple entries with the same value for key
    /// return: first: vector of multiple values found
    ///         second: vector of vectors of indices where first value was found
    std::pair< vector< string >, vector< vector< unsigned > > > findMultipleEntries(string const& key) const;

    /// find multiple entries with the same <key> and mean combine the values from
    /// <keysToCombine> which must be convertible to float if they exist
    CSVData combineMultipleEntries(string const& key, vector<string> const& keysToCombine, string const& filename) const;

    /// find value in column <keyword>
    /// returns indices of all occurances of value if found, otherwise returns [-1]
    vector<int> find(string const& keyword, string const& value, int startIndex=0) const;

    void printHeader() const;
/*    void setDataSize(int nCols, int nStars){
        data.resize(nCols);
        for (auto itDat=data.begin(); itDat!=data.end(); ++itDat)
            itDat->resize(nStars);
        return;
    }*/
};

inline bool is_file_exist(string const& fileName)
{
    std::ifstream infile(fileName.c_str());
    return infile.good();
}

vector<string> readHeader(string const& fileName, char const& delimiter=',');

vector<int> countCharPerLine(string const& fileName, char const& character);

void writeStrVecToFile(vector<string> const& strVec, ofstream& outFile);

CSVData readCSVFile(string const& fileName, char const& delimiter, bool const& removeBadLines);
CSVData readCSVFile(string const& fileName);

void writeCSVFile(CSVData const& dat, string const& fileName);
vector<string> splitCSVLine(string const& line, char const& delimiter=',');

vector<double> convertStringVectorToDoubleVector(vector<string> const& stringVector);
vector<float> convertStringVectorToFloatVector(vector<string> const& stringVector);
vector<unsigned> convertStringVectorToUnsignedVector(vector<string> const& stringVector);
vector<string> convertDoubleVectorToStringVector(vector<double> const& doubleVector);

void appendFile(string const& inFileName, string const& outFileName);

CSVData crossMatch(CSVData const& csvDataA, CSVData const& csvDataB, string const& key);

vector<double> getGaiaG(CSVData const& csvData);

bool isEven(int n);

/// find first occurance of <element> in <vecOfElements>
/// return.first: bool: found yes or no
/// return.second: index of first occurance, -1 if return.first == false
template < typename T >
std::pair<bool, int> findInVector(const std::vector<T> & vecOfElements, const T& element);

double mean(vector< double > const& valVec);

#endif
