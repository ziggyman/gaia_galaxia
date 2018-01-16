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

    string getData(string const& keyword, int row) const{
        int headerPos = findKeywordPos(keyword);
        if (headerPos < 0){
            cout << "ERROR: keyword <" << keyword << "> not found" << endl;
            exit(EXIT_FAILURE);
        }
        return data[row][headerPos];
    }

    vector<string> getData(string const& keyword) const{
        int headerPos = findKeywordPos(keyword);
        if (headerPos < 0){
            cout << "ERROR: keyword <" << keyword << "> not found" << endl;
            exit(EXIT_FAILURE);
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
                cout << "getData: ERROR thrown: iRow = " << iRow << ", headerPos = " << headerPos << ", data.size() = " << data.size() << ", data[" << iRow << "].size() = " << data[iRow].size() << endl;
                for (int i=0; i<data[iRow].size(); ++i)
                    cout << "data[" << iRow << "][" << i << "] = " << data[iRow][i] << endl;
                exit(EXIT_FAILURE);
            }
//            cout << "CSVData.getData(): setting out[ = " << out.size() << "] to " << outStr << endl;
        }
        cout << "CSVData.getData(): out.size() = " << out.size() << endl;
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

vector<double> convertStringVectortoDoubleVector(const vector<string>& stringVector);

#endif
