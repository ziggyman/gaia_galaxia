#include "csvData.h"

int CSVData::findKeywordPos(string const& keyword) const{
    int keywordPos = -1;
    for (int headerPos=0; headerPos<header.size(); ++headerPos){
        if (keyword.compare(header[headerPos]) == 0)
            keywordPos = headerPos;
    }
    return keywordPos;
}

vector<string> CSVData::getData(unsigned row) const{
    if (size() == 0){
        throw std::runtime_error("CSVData::getData(int): ERROR: data is empty");
    }
    if (row >= size()){
        throw std::runtime_error("CSVData::getData(int): ERROR: row(="
                +to_string(row)+") >= size(="+to_string(size())+")");
    }
    return vector<string>(data[row]);
}

vector<string> CSVData::getData(unsigned row){
    if (size() == 0){
        throw std::runtime_error("CSVData::getData(int): ERROR: data is empty");
    }
    if (row >= size()){
        throw std::runtime_error("CSVData::getData(int): ERROR: row(="
                +to_string(row)+") >= size(="+to_string(size())+")");
    }
    return data[row];
}

string CSVData::getData(string const& keyword, int row) const{
    int headerPos = findKeywordPos(keyword);
    if (headerPos < 0){
        /// mayge it's the G color...
        if (keyword.compare("G") == 0){
            /// TODO: here we should actually require the G values to be present
            /// somewhere as a vector and not calculate it again each time
            /// for the whole data set. For now it works but it will be
            /// extremely slow if we ask for the G values of lots of rows...
            return to_string(getGaiaG(*this)[row]);
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

vector<string> CSVData::getData(string const& keyword) const{
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

void CSVData::setData(vector< vector< string > > & dataIn){
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

void CSVData::addColumn(string const& colName, vector<string> const& colData){
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

void CSVData::addColumn(string const& colName, vector<double> const& colData){
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

int CSVData::size() const{
    return data.size();
}

void CSVData::append(vector<string> const& newLine){
    if (newLine.size() != header.size()){
        throw std::runtime_error("CSVData::append: ERROR newLine.size() = "
                + to_string(newLine.size()) + " != header.size() = " + to_string(header.size()));
    }
    data.push_back(newLine);
}

void CSVData::printHeader() const{
    cout << header[0];
    for (int i=1; i<header.size(); ++i)
        cout << ", " << header[i];
    cout << endl;
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

vector<int> countCharPerLine(string const& fileName, char const& character){
    ifstream inStream(fileName);
    vector<int> occurances;
    if (inStream.is_open()){
        string line;
        while(inStream.good()){
            if (getline(inStream, line)){
                occurances.push_back(std::count(line.begin(), line.end(), character));
            }
        }
    }
    return occurances;
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

CSVData readCSVFile(string const& fileName, bool const& removeBadLines){
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
            int nCommas = 0;
            int nQuotes = count(line.begin(), line.end(), '"');
            if (!isEven(nQuotes)){
                throw std::runtime_error("found uneven number of quotes in line <"+line+">");
            }
            if (nQuotes > 0){
                stringstream lineStream(line.c_str());
                while(lineStream.good()){
                    getline(lineStream, substring, '"');
//                    cout << "header: pos = " << pos << ": substring = " << substring << endl;
                    nCommas += count(substring.begin(), substring.end(), ',');
                    if (lineStream.good())
                        getline(lineStream, substring, '"');
                }
            }
            else
                nCommas = count(line.begin(), line.end(), ',');
//            cout << "line contains " << nCommas << " kommas" << endl;
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
            if (nCommas != csvData.header.size()-1){
                cout << "readCSVFile: ERROR: nCommas = " << nCommas << " != csvData.header.size()-1 = " << csvData.header.size()-1 << endl;
                cout << "previousLine = " << previousLine << endl;
                cout << "line = " << line << endl;
                if (!removeBadLines)
                    exit(EXIT_FAILURE);
            }
            else{
                vector<string> dataLine(0);
                stringstream lineStream(line.c_str());
                pos = 0;
                if (nQuotes > 0){
                    while(lineStream.good()){
                        getline(lineStream, substring, '"');
                        if (lineStream.good())//There was a quote, remove the last comma before the quote
                            substring = substring.substr(0,substring.length()-1);
    //                    cout << "header: substring = " << substring << endl;
                        stringstream subStream(substring);
                        while (subStream.good()){
                            getline(subStream, substring, ',');
    //                        cout << "header: pos = " << pos << ": substring = " << substring << endl;
                            dataLine.push_back(substring);
                            pos++;
                        }
                        if (lineStream.good()){
                            getline(lineStream, substring, '"');
    //                        cout << "header: pos = " << pos << ": substring = " << substring << endl;
                            dataLine.push_back(substring);
                            pos++;
                            if (lineStream.good())
                                getline(lineStream, substring, ',');//Remove first comma after the 2nd quote
                        }
                    }
                }
                else{
                    while(lineStream.good()){
                        getline(lineStream, substring, ',');
        //                cout << "pos = " << pos << ": substring = " << substring << endl;
                        dataLine.push_back(substring);
                        pos++;
                    }
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

vector<double> getGaiaG(CSVData const& csvData){
    vector<string> filters = splitCSVLine(modelGetFilters());
//    cout << "filters = [";
//    for (auto i: filters) cout << i << ", ";
//    cout << "]" << endl;
    vector<double> gaiaG(0);

    if (getPhotometricSystem().compare("SDSS") == 0){
        vector<double> sdss_g;
        vector<double> sdss_r;
        vector<double> sdss_i;
        for (auto itFilter = filters.begin(); itFilter != filters.end(); ++itFilter){
            if (itFilter->compare("g") == 0)
                sdss_g = convertStringVectorToDoubleVector(csvData.getData(modelGetFilterKeyWord("g")));
            else if (itFilter->compare("g") == 0)
                sdss_r = convertStringVectorToDoubleVector(csvData.getData(modelGetFilterKeyWord("r")));
            else if (itFilter->compare("i") == 0)
                sdss_i = convertStringVectorToDoubleVector(csvData.getData(modelGetFilterKeyWord("i")));
        }

    //    cout << "getGaiaG: min(sdss_g) = " << *min_element(sdss_g.begin(), sdss_g.end()) << ", max(sdss_g) = " << *max_element(sdss_g.begin(), sdss_g.end()) << endl;
        gaiaG = calcGaiaGFromgri(sdss_g, sdss_r, sdss_i);
    }
    else if (getPhotometricSystem().compare("UBV") == 0){
        vector<double> ubv_b;
        vector<double> ubv_v;
        vector<double> ubv_i;
        for (auto itFilter = filters.begin(); itFilter != filters.end(); ++itFilter){
            if (itFilter->compare("B") == 0){
                ubv_b = convertStringVectorToDoubleVector(csvData.getData(modelGetFilterKeyWord("B")));
            }
            else if (itFilter->compare("V") == 0){
                ubv_v = convertStringVectorToDoubleVector(csvData.getData(modelGetFilterKeyWord("V")));
            }
            else if (itFilter->compare("I") == 0){
                ubv_i = convertStringVectorToDoubleVector(csvData.getData(modelGetFilterKeyWord("I")));
            }
        }

        gaiaG = calcGaiaGFromVI(ubv_v, ubv_i);
    }
    cout << "getGaiaG: min(gaiaG) = " << *min_element(gaiaG.begin(), gaiaG.end()) << ", max(gaiaG) = " << *max_element(gaiaG.begin(), gaiaG.end()) << endl;
    return gaiaG;
}

bool isEven(int n){
    return (n % 2 == 0);
}
