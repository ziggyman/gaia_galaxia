#ifndef __GALCOMP_H__
#define __GALCOMP_H__

#include "hammer.h"
#include <iostream>
#include <fstream>
#include <string>
#include <sys/time.h>
#include <vector>

using namespace std;

struct CSVData{
    vector<string> header;
    vector< vector< string > > data;

    int findKeywordPos(string const& keyword){
        int keywordPos = -1;
        for (int headerPos=0; headerPos<header.size(); ++headerPos){
            if (keyword.compare(header[headerPos]) == 0)
                keywordPos = headerPos;
        }
        return keywordPos;
    }

    string getData(string const& keyword, int row){
        int headerPos = findKeywordPos(keyword);
        if (headerPos < 0){
            cout << "ERROR: keyword <" << keyword << "> not found" << endl;
            exit(EXIT_FAILURE);
        }
        return data[row][headerPos];
    }

    vector<string> getData(string const& keyword){
        int headerPos = findKeywordPos(keyword);
        if (headerPos < 0){
            cout << "ERROR: keyword <" << keyword << "> not found" << endl;
            exit(EXIT_FAILURE);
        }
        vector<string> out(data.size());
        for (int iRow=0; iRow<data.size(); ++iRow)
            out[iRow] = data[iRow][headerPos];
        return out;
    }
};

void countStars(string const& dir, string const& fileNameRoot, bool zeroToThreeSixty){
    vector<Pixel> pixels = getPixels();
    
}

vector<string> readHeader(string const& fileName){
    ifstream inStream(fileName);
    vector<string> header(0);
    string substring;
    if (inStream.is_open()){
        string line;
        if (getline(inStream, line)){
            stringstream lineStream(line.c_str());
            while(lineStream.good()){
                getline(lineStream, substring, ',');
                header.push_back(substring);
//                cout << "readHeader: header[" << header.size()-1 << "] = " << header[header.size()-1] << endl;
            }
        }
        inStream.close();
        cout << "readHeader: inStream closed" << endl;
    }
    else{
        cout << "ERROR: Could not open file <" << fileName << ">" << endl;
        exit(EXIT_FAILURE);
    }
    return header;
}

void writeStrVecToFile(vector<string> const& strVec, ofstream& outFile){
    string strToWrite(strVec[0]);
    for (int iStr=1; iStr<strVec.size(); ++iStr){
        strToWrite.append(",");
        strToWrite.append(strVec[iStr]);
    }
    outFile.write(strToWrite.c_str(), strlen(strToWrite.c_str()));
    return;
}

CSVData readCSVFile(string const& fileName){
    ifstream inStream(fileName);
    if (inStream.is_open()){
        cout << "file with name <" << fileName << "> is open" << endl;
    }
    else{
        cout << "file with name <" << fileName << "> is not open" << endl;
        exit(EXIT_FAILURE);
    }
    CSVData csvData;
    int pos;
    string substring;
    struct timeval start, end;

    gettimeofday(&start, NULL);

    if (inStream.is_open()){
        int iLine = 0;
        string line;
        while (getline(inStream, line)){
            if (iLine == 0){
                stringstream lineStream(line.c_str());
                pos = 0;
                while(lineStream.good()){
                    getline(lineStream, substring, ',');
//                    cout << "header: pos = " << pos << ": substring = " << substring << endl;
                    csvData.header.push_back(substring);
//                    cout << "pos = " << pos << ": added " << csvData.header[csvData.header.size()-1] << " to header" << endl;
                    pos++;
                }
                iLine = 1;
                continue;
            }
            stringstream lineStream(line.c_str());
            pos = 0;
            vector<string> dataLine(0);
            while(lineStream.good()){
                getline(lineStream, substring, ',');
//                cout << "pos = " << pos << ": substring = " << substring << endl;
                dataLine.push_back(substring);
                pos++;
            }
            csvData.data.push_back(dataLine);
        }
        inStream.close();
        gettimeofday(&end, NULL);
        cout << "fileName <" << fileName << "> read in " << ((end.tv_sec * 1000000 + end.tv_usec)
                        - (start.tv_sec * 1000000 + start.tv_usec))/1000000 << " s" << endl;
        cout << "csvData.data.size() = " << csvData.data.size() << endl;
    }
    else{
        cout << "ERROR: fileName <" << fileName << "> not open" << endl;
        exit(EXIT_FAILURE);
    }
    return csvData;
}

vector<double> convertStringVectortoDoubleVector(const vector<string>& stringVector){
    vector<double> doubleVector(0);
    for (vector<string>::const_iterator iter = stringVector.begin(); iter != stringVector.end(); ++iter){
        string const& element = *iter;
        std::istringstream is(element);
        double result;
        is >> result;
        doubleVector.push_back(result);
    }
    return doubleVector;
}

#endif
