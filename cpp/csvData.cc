#include "csvData.h"

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
    string endOfLine("\n");
    outFile.write(endOfLine.c_str(), strlen(endOfLine.c_str()));
    return;
}

CSVData readCSVFile(string const& fileName){
    ifstream inStream(fileName);
    if (!inStream.is_open()){
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
        string line, previousLine;
        while (getline(inStream, line)){
            int nKommas = count(line.begin(), line.end(), ',');
//            cout << "line contains " << nKommas << " kommas" << endl;
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
                previousLine = line;
                cout << "readCSVFile: " << fileName << " contains " << csvData.header.size() << " columns" << endl;
                continue;
            }
            if (nKommas != csvData.header.size()-1){
                cout << "readCSVFile: ERROR: nKommas = " << nKommas << " != csvData.header.size() = " << csvData.header.size() << endl;
                cout << "previousLine = " << previousLine << endl;
                cout << "line = " << line << endl;
                exit(EXIT_FAILURE);
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
            if (dataLine.size() != csvData.header.size()){
                cout << "readCSVFile: ERROR: dataLine.size() = " << dataLine.size() << " != csvData.header.size() = " << csvData.header.size() << endl;
                cout << "line = " << line << endl;
                for (int i=0; i<dataLine.size(); ++i)
                    cout << "dataLine[" << i << "] = " << dataLine[i] << endl;
                exit(EXIT_FAILURE);
            }
            csvData.data.push_back(dataLine);
            previousLine = line;
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

vector<double> convertStringVectorToDoubleVector(vector<string> const& stringVector){
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

vector<float> convertStringVectorToFloatVector(vector<string> const& stringVector){
    vector<float> floatVector(0);
    for (vector<string>::const_iterator iter = stringVector.begin(); iter != stringVector.end(); ++iter){
        string const& element = *iter;
        std::istringstream is(element);
        float result;
        is >> result;
        floatVector.push_back(result);
    }
    return floatVector;
}

vector<unsigned> convertStringVectorToUnsignedVector(vector<string> const& stringVector){
    vector<unsigned> outVector(0);
    for (vector<string>::const_iterator iter = stringVector.begin(); iter != stringVector.end(); ++iter){
        string const& element = *iter;
        std::istringstream is(element);
        unsigned result;
        is >> result;
        outVector.push_back(result);
    }
    return outVector;
}

vector<string> convertDoubleVectorToStringVector(vector<double> const& doubleVector){
    vector<string> stringVector(0);
    stringVector.reserve(doubleVector.size());
    for (vector<double>::const_iterator iter = doubleVector.begin(); iter != doubleVector.end(); ++iter){
        stringVector.push_back(to_string(*iter));
        cout << "convertDoubleVectorToStringVector: *iter = " << *iter << ": stringVector["
                << stringVector.size()-1 << "] = " << stringVector[stringVector.size()-1] << endl;
    }
    return stringVector;
}

vector<string> splitCSVLine(string const& line){
    string tmpStr(line);
    cout << "splitCSVLine: tmpStr = " << tmpStr << endl;
    vector<string> out(0);
    size_t kommaPos = tmpStr.find(",");
    cout << "splitCSVLine: kommaPos = " << kommaPos << endl;
    while (kommaPos != string::npos){
        out.push_back(tmpStr.substr(0,kommaPos));
        tmpStr = tmpStr.substr(kommaPos+1);
        cout << "splitCSVLine: tmpStr = " << tmpStr << endl;
        kommaPos = tmpStr.find(",");
        cout << "splitCSVLine: kommaPos = " << kommaPos << endl;
    }
    out.push_back(tmpStr);
    return out;
}

void appendFile(string const& inFileName, string const& outFileName){
    std::ifstream inFile(inFileName);
    std::ofstream outFile(outFileName, std::ios_base::app | std::ios_base::out);
    std::string   line;

    while(std::getline(inFile, line))
    {
        outFile << line;
    }
    outFile.close();
}
