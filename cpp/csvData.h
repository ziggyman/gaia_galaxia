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

    string getData(string const& keyword, int row) const;

    vector<string> getData(string const& keyword) const;

    void setData(vector< vector< string > > & dataIn);

    void addColumn(string const& colName, vector<string> const& colData);

    void addColumn(string const& colName, vector<double> const& colData);

    int size() const;

    void append(vector<string> const& newLine);

    void printHeader() const;
/*    void setDataSize(int nCols, int nStars){
        data.resize(nCols);
        for (auto itDat=data.begin(); itDat!=data.end(); ++itDat)
            itDat->resize(nStars);
        return;
    }*/
};

vector<string> readHeader(string const& fileName);

vector<int> countCharPerLine(string const& fileName, char const& character);

void writeStrVecToFile(vector<string> const& strVec, ofstream& outFile);

CSVData readCSVFile(string const& fileName, bool const& removeBadLines=true);
void writeCSVFile(CSVData const& dat, string const& fileName);
vector<string> splitCSVLine(string const& line);

vector<double> convertStringVectorToDoubleVector(vector<string> const& stringVector);
vector<float> convertStringVectorToFloatVector(vector<string> const& stringVector);
vector<unsigned> convertStringVectorToUnsignedVector(vector<string> const& stringVector);
vector<string> convertDoubleVectorToStringVector(vector<double> const& doubleVector);

void appendFile(string const& inFileName, string const& outFileName);

CSVData crossMatch(CSVData const& csvDataA, CSVData const& csvDataB, string const& key);

vector<double> getGaiaG(CSVData const& csvData);

bool isEven(int n);

#endif
