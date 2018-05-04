#ifndef __CSVDATA_H__
#define __CSVDATA_H__

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <sys/time.h>
#include <vector>

using namespace std;

struct CSVData{
    vector<string> header;
    vector< vector< string > > data;

    int findKeywordPos(string const& keyword) const{
        int keywordPos = -1;
        for (int headerPos=0; headerPos<header.size(); ++headerPos){
            if (keyword.compare(header[headerPos]) == 0)
                keywordPos = headerPos;
        }
        return keywordPos;
    }

    vector<string> getData(unsigned row) const{
        if (size() == 0){
            throw std::runtime_error("CSVData::getData(int): ERROR: data is empty");
        }
        if (row >= size()){
            throw std::runtime_error("CSVData::getData(int): ERROR: row(="
                    +to_string(row)+") >= size(="+to_string(size())+")");
        }
        return vector<string>(data[row]);
    }

    vector<string> getData(unsigned row){
        if (size() == 0){
            throw std::runtime_error("CSVData::getData(int): ERROR: data is empty");
        }
        if (row >= size()){
            throw std::runtime_error("CSVData::getData(int): ERROR: row(="
                    +to_string(row)+") >= size(="+to_string(size())+")");
        }
        return data[row];
    }

    string getData(string const& keyword, int row) const{
        int headerPos = findKeywordPos(keyword);
        if (headerPos < 0){
            /// mayge it's the G color...
            if (keyword.compare("G") == 0){
                /// TODO: here we should actually require the G values to be present
                /// somewhere as a vector and not calculate it again each time
                /// for the whole data set. For now it works but it will be
                /// extremely slow if we ask for the G values of lots of rows...
                return string(getGaiaG(*this)[row]);
            }
            else
            throw std::runtime_error("CSVData::getData: ERROR: keyword <" + keyword + "> not found");
        }
        if (size() == 0){
            throw std::runtime_error("CSVData::getData(int): ERROR: data is empty");
        }
        if (row >= size()){
            throw std::runtime_error("CSVData::getData(int): ERROR: row(="
                    +to_string(row)+") >= size(="+to_string(size())+")");
        }
        return data[row][headerPos];
    }

    vector<string> getData(string const& keyword) const{
        cout << "CSVData::getData(keyword=" << keyword << ")" << endl;
        int headerPos = findKeywordPos(keyword);
        if (headerPos < 0){
            /// mayge it's the G color...
            if (keyword.compare("G") == 0){
                /// a little complicated returning a string vector of a double vector
                /// only to convert it to float or double again later...
                return convertDoubleVectorToStringVector(getGaiaG(*this));
            }
            else
                throw std::runtime_error("CSVData::getData: ERROR: keyword <" + keyword + "> not found");
        }
        cout << "CSVData.getData(): size() = " << size() << endl;
        vector<string> out(0);
        out.reserve(size());
        for (int iRow=0; iRow<size(); ++iRow){
            if ((iRow >= size()) || (iRow < 0)){
                cout << "getData: ERROR: iRow = " << iRow << " outside limits" << endl;
                exit(EXIT_FAILURE);
            }
            if ((headerPos < 0) || (headerPos >= data[0].size())){
                cout << "getData: ERROR: headerPos = " << headerPos << " outside limits" << endl;
            }
            try{
                string outStr((data[iRow])[headerPos]);
                out.push_back(outStr);
            }
            catch(...){
                string message("getData: ERROR thrown: iRow = ");
                message += to_string(iRow) + ", headerPos = " + to_string(headerPos) +
                        ", data.size() = " + to_string(size()) + ", data[" +
                        to_string(iRow) + "].size() = " + to_string(data[iRow].size()) + "\n";
                for (int i=0; i<data[iRow].size(); ++i)
                    message += "data[" + to_string(iRow) + "][" + to_string(i) + "] = " + data[iRow][i] + "\n";
                throw std::runtime_error(message);
            }
//            cout << "CSVData.getData(): setting out[ = " << out.size() << "] to " << outStr << endl;
        }
//        cout << "CSVData.getData(): out.size() = " << out.size() << endl;
        return out;
    }

    void setData(vector< vector< string > > & dataIn){
        int nStars = dataIn.size();
        data.resize(nStars);
        int nCols = dataIn[0].size();
        for (auto itIn=dataIn.begin(), it=data.begin();
             itIn!= dataIn.end();
             ++itIn, ++it){
            it->resize(nCols);
            *it = *itIn;
        }
    }

    void addColumn(string const& colName, vector<string> const& colData){
        if (colData.size() != size()){
            throw std::runtime_error("CSVData::addColumn: ERROR: colData.size() = "
                    + to_string(colData.size()) + " != size() = " + to_string(size()));
        }
//        cout << "CSVData::addColumn: colName = <" << colName << ">" << endl;
        header.push_back(colName);
        auto itColData = colData.begin();
        int iColData = 0;
        for (auto itData=data.begin(); itData != data.end(); ++itData, ++itColData){
//            cout << "CSVData::addColumn: itData->size() = " << itData->size() << " *itColData = " << *itColData << ", colData[" << iColData << "] = " << colData[iColData] << endl;
            itData->push_back(*itColData);
//            cout << "CSVData::addColumn: itData->size() = " << itData->size() << endl;
//            throw std::runtime_error("let's exit");
        }
//        return data;
    }

    void addColumn(string const& colName, vector<double> const& colData){
        if (colData.size() != size()){
            throw std::runtime_error("CSVData::addColumn: ERROR: colData.size() = "
                    + to_string(colData.size()) + " != size() = " + to_string(size()));
        }
//        cout << "CSVData::addColumn: colName = <" << colName << ">" << endl;
        header.push_back(colName);
        auto itColData = colData.begin();
        int iColData = 0;
        for (auto itData=data.begin(); itData != data.end(); ++itData, ++itColData){
//            cout << "CSVData::addColumn: itData->size() = " << itData->size() << " *itColData = " << *itColData << ", colData[" << iColData << "] = " << colData[iColData] << endl;
            itData->push_back(to_string(*itColData));
//            cout << "CSVData::addColumn: itData->size() = " << itData->size() << endl;
//            throw std::runtime_error("let's exit");
        }
//        return data;
    }

    int size() const{
        return data.size();
    }

/*    void setDataSize(int nCols, int nStars){
        data.resize(nCols);
        for (auto itDat=data.begin(); itDat!=data.end(); ++itDat)
            itDat->resize(nStars);
        return;
    }*/
};

vector<string> readHeader(string const& fileName);

void writeStrVecToFile(vector<string> const& strVec, ofstream& outFile);

CSVData readCSVFile(string const& fileName);
vector<string> splitCSVLine(string const& line);

vector<double> convertStringVectorToDoubleVector(vector<string> const& stringVector);
vector<float> convertStringVectorToFloatVector(vector<string> const& stringVector);
vector<unsigned> convertStringVectorToUnsignedVector(vector<string> const& stringVector);
vector<string> convertDoubleVectorToStringVector(vector<double> const& doubleVector);

void appendFile(string const& inFileName, string const& outFileName);

#endif
