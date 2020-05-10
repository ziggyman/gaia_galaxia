#include "csvData.h"

int CSVData::findKeywordPos(string const& keyword) const{
    int keywordPos = 0;
    for (auto itHeader=header.begin(); itHeader != header.end(); ++itHeader, ++keywordPos){
        if (itHeader->compare(keyword) == 0)//{
            return keywordPos;
    }
    return -1;
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

vector< vector< string > > CSVData::getData(vector<unsigned> const& rows) const{
    vector< vector< string > > outCSVData(0);
    for (int i = 0; i < rows.size(); ++i){
        outCSVData.push_back(getData(rows[i]));
    }
    return outCSVData;
}

vector< vector< string > > CSVData::getData(vector<int> const& rows) const{
    vector< vector< string > > outCSVData(0);
    for (int i = 0; i < rows.size(); ++i){
        outCSVData.push_back(getData(rows[i]));
    }
    return outCSVData;
}

string CSVData::getData(string const& keyword, unsigned row) const{
    int headerPos = findKeywordPos(keyword);
    if (headerPos < 0){
        /// mayge it's the G color...
//        if (keyword.compare("G") == 0){
            /// TODO: here we should actually require the G values to be present
            /// somewhere as a vector and not calculate it again each time
            /// for the whole data set. For now it works but it will be
            /// extremely slow if we ask for the G values of lots of rows...
//            return to_string(getGaiaG(*this)[row]);
//        }
//        else
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
//    cout << "CSVData::getData(keyword=" << keyword << ")" << endl;
    int headerPos = findKeywordPos(keyword);
    if (headerPos < 0){
        /// mayge it's the G color...
//        if (keyword.compare("G") == 0){
            /// a little complicated returning a string vector of a double vector
            /// only to convert it to float or double again later...
//            return convertDoubleVectorToStringVector(getGaiaG(*this));
//        }
//        else
            throw std::runtime_error("CSVData::getData: ERROR: keyword <" + keyword + "> not found");
    }
//    cout << "CSVData.getData(): size() = " << size() << endl;
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

vector<string> CSVData::getData(string const& keyword, vector<unsigned> const& rows) const{
    vector< string > out(0);
    int pos = findKeywordPos(keyword);
    if (pos < 0){
        throw std::runtime_error("getData: ERROR: keyword <"+keyword+"> not found in header\n");
    }
    for (auto it=rows.begin(); it!=rows.end(); ++it){
        if (*it >= size())
            throw std::runtime_error("getData: ERROR: row "+to_string(*it)+" > size(="+to_string(size())+")\n");
        out.push_back(data[*it][pos]);
    }
    return out;
}

vector<string> CSVData::getData(string const& keyword, vector<int> const& rows) const{
    vector< string > out(0);
    int pos = findKeywordPos(keyword);
    if (pos < 0){
        throw std::runtime_error("getData: ERROR: keyword <"+keyword+"> not found in header\n");
    }
    for (auto it=rows.begin(); it!=rows.end(); ++it){
        if (*it >= size())
            throw std::runtime_error("getData: ERROR: row "+to_string(*it)+" > size(="+to_string(size())+")\n");
        out.push_back(data[*it][pos]);
    }
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

void CSVData::setData(string const& keyword, unsigned row, string const& value){
    data[row][findKeywordPos(keyword)] = value;
}

void CSVData::addColumn(string const& colName){
    header.push_back(colName);
    for (auto itData=data.begin(); itData != data.end(); ++itData){
        itData->push_back(string(""));
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

void CSVData::removeColumn(string const& colName){
    int keywordPos = findKeywordPos(colName);
    header.erase(header.begin()+keywordPos);
    for (auto itData=data.begin(); itData != data.end(); ++itData){
        itData->erase(itData->begin()+keywordPos);
    }
}

void CSVData::renameColumn(string const& oldName, string const& newName){
    int keywordPos = findKeywordPos(oldName);
    if (keywordPos < 0){
        throw std::runtime_error("CSVData::renameColumn: ERROR: oldName = "
                + oldName + " not found in header");
    }
    header[keywordPos] = newName;
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
    //cout << "new line appended to this->data: this->size() = " << size() << endl;
}

void CSVData::append(vector< vector< string > > const& newLines){
    for (auto it=newLines.begin(); it!=newLines.end(); ++it)
        this->append(*it);
}

void CSVData::append(CSVData const& csv){
    for (unsigned i = 0; i < header.size(); ++i){
        if (std::find(csv.header.begin(), csv.header.end(),header[i]) == csv.header.end())
            throw std::runtime_error("CSVData::append: ERROR: headers are not the same: header keyword <"+header[i]+"> not found in csv");
    }
    for (unsigned i = 0; i < csv.size(); ++i){
        vector<string> newLine(0);
        for (unsigned j = 0; j < csv.header.size(); ++j)
            newLine.push_back(csv.getData(header[j],i));
        data.push_back(newLine);
    }
}

vector<int> CSVData::find(string const& keyword, string const& value, long startIndex) const{
    cout << "CSVData::find: keyword = " << keyword << ", value = " << value << ", startIndex = " << to_string(startIndex) << endl;
    unsigned keywordPos = findKeywordPos(keyword);
    vector<int> vecOut(0);
    bool found = false;
    int startIndexTemp = startIndex;
    if (startIndexTemp < 0){
        cout << "CSVData::find: PROBLEM: startIndex < 0" << endl;
        startIndexTemp = 0;
    }
    long i = startIndexTemp;
    cout << "CSVData::find: i = " << to_string(startIndexTemp) << endl;
    cout << "CSVData::find: this->size() = " << to_string(this->size()) << endl;
    if ((this->size() == 0) || (this->size() <= startIndexTemp)){
        vecOut.push_back(-1);
        return vecOut;
    }
    for (auto it = data.begin()+startIndexTemp; it != data.end(); ++it, ++i){
//        cout << "CSVData::find: it = " << it - data.begin() << endl;
        if ((*it)[keywordPos].compare(value) == 0){
            vecOut.push_back(i);
            found = true;
            cout << "CSVData::find: value <" << value << "> found at position " << to_string(i) << endl;
        }
    }
    if (found){
        cout << "CSVData::find: found == True" << endl;
        return vecOut;
    }
    cout << "CSVData::find: found == False" << endl;
    vecOut.push_back(-1);
    return vecOut;
}

void CSVData::removeRow(unsigned row){
    if (row >= size()){
        throw std::runtime_error("CSVData::removeRow: ERROR: row(="+to_string(row)+") >= size(="+to_string(size())+")");
    }
    data.erase(data.begin()+row);
}

std::pair< vector< string >, vector< vector< unsigned > > > CSVData::findMultipleEntries(string const& key) const{
    cout << "findMultipleEntries(key = <" << key << ">) started: this->size() = " << size() << endl;
    std::pair< vector< string >, vector< vector< unsigned > > > out;
    vector< vector< unsigned > > multipleEntries(0);
    vector<string> alreadyChecked(0);
    int pos = findKeywordPos(key);
    cout << "findMultipleEntries: pos = " << pos << endl;
    if (pos < 0){
        throw std::runtime_error("CSVData::findMultipleEntries: ERROR: keyword <" + key + "> not found");
    }
    string value;
    for (auto it=data.begin(); it!=data.end(); ++it){
        value = (*it)[pos];
        cout << "findMultipleEntries: value = " << value << endl;
        if (!findInVector(alreadyChecked, value).first){
            vector<int> positions = find(key, value);
            cout << "findMultipleEntries: positions = ";
            for (int i = 0; i < positions.size(); ++i)
                cout << positions[i] << ", ";
            cout << endl;
            if (positions.size() > 1){
                alreadyChecked.push_back(value);
                vector<unsigned> upos(0);
                for (auto itPos=positions.begin(); itPos!=positions.end(); ++itPos)
                    upos.push_back((unsigned int)(*itPos));
                cout << "findMultipleEntries: upos = ";
                for (int i = 0; i < upos.size(); ++i)
                    cout << upos[i] << ", ";
                cout << endl;
                multipleEntries.push_back(vector<unsigned>(upos));
            }
        }
    }
    out.first = alreadyChecked;
    out.second = multipleEntries;
    for (int i=0; i<alreadyChecked.size(); ++i){
        cout << "findMultipleEntries: alreadyChecked[" << i << "] = " << out.first[i] << ", multipleEntries[" << i << "] = ";
        for (int j=0; j<out.second.size(); ++j){
            cout << out.second[i][j] << ", ";
        }
        cout << endl;
    }
    return out;
}

CSVData CSVData::combineMultipleEntries(string const& key, vector<string> const& keysToCombine, string const& filename) const{
    cout << "combineMultipleEntries: this->size() = " << size() << endl;
    cout << "combineMultipleEntries: this->header = ";
    for (int i=0; i<header.size(); ++i)
        cout << header[i] << ", ";
    cout << endl;
//    cout << "combineMultipleEntries: data = ";
//    for (int i=0; i<size(); ++i){
//        for (int j=0; j<header.size(); ++j)
//            cout << data[i][j];
//        cout << endl;
//    }

//    cout << "combineMultipleEntries: key = <" << key << ">" << endl;
//    cout << "combineMultipleEntries: keysToCombine = <";
//    for (int i=0; i<keysToCombine.size(); ++i)
//        cout << keysToCombine[i] << ",";
//    cout << ">" << endl;

//    string tempKey = "source_id";
//    vector<string> tempKeysToCombine(0);
//    tempKeysToCombine.push_back("umag");
//    tempKeysToCombine.push_back("gmag");
//    tempKeysToCombine.push_back("rmag");
//    tempKeysToCombine.push_back("imag");
//    tempKeysToCombine.push_back("zmag");
//    cout << "combineMultipleEntries: tempKey = <" << tempKey << ">" << endl;
//    cout << "combineMultipleEntries: tempKeysToCombine = <";
//    for (int i=0; i<tempKeysToCombine.size(); ++i)
//        cout << tempKeysToCombine[i] << ",";
//    cout << ">" << endl;

//    std::pair< vector< string >, vector< vector< unsigned > > > multipleEntries = findMultipleEntries(key);
    CSVData csvOut;
    csvOut.header = header;
    vector< string > done(0);
    int pos = findKeywordPos(key);
    cout << "combineMultipleEntries: keywordPos = " << pos << endl;

    std::ofstream myfile;
    string outStr;
    if (is_file_exist(filename)){
        CSVData csvIn = readCSVFile(filename, ",", true);
        for (int i = 0; i < csvIn.size(); ++i)
            done.push_back(csvIn.getData(key, i));
        myfile.open(filename, fstream::app);
    }
    else{
        myfile.open(filename, fstream::out);

        ///write header
        outStr = header[0];
        for (int i=1; i<header.size(); i++){
            outStr += ","+header[i];
        }
        outStr += "\n";
        myfile << outStr;
    }

    /// for each row in data
    int iRow = 0;
    for (auto it=data.begin(); it!=data.end(); ++it, ++iRow){
        /// check if already done
        if ((done.size() == 0) || (::find(done.begin(), done.end(), (*it)[pos]) == done.end())){
            cout << "combineMultipleEntries: object not done yet" << endl;
            csvOut.append(*it);

            vector<int> positions = find(key, (*it)[pos], iRow);
            cout << "combineMultipleEntries: iRow = " << iRow << endl;

            /// if multiple entries exist for this object
//            std::pair< bool, int > found = findInVector(multipleEntries.first, (*it)[pos]);
            if (positions.size() > 1){
                /// take mean of values for keysToCombine
                for (auto itKeyToCombine=keysToCombine.begin();
                     itKeyToCombine!=keysToCombine.end();
                     ++itKeyToCombine)
                {
                    int keyPos = findKeywordPos(*itKeyToCombine);
                    cout << "combineMultipleEntries: calculating mean value of key " << *itKeyToCombine << endl;

                    vector<string> dat = getData(*itKeyToCombine, positions);
                    vector<double> datD(0);
                    for (vector<string>::const_iterator iter = dat.begin(); iter != dat.end(); ++iter){
                        if (iter->compare("") != 0){
                            string const& element = *iter;
                            std::istringstream is(element);
                            double result;
                            is >> result;
                            datD.push_back(result);
                            cout << "combineMultipleEntries: added " << to_string(result) << " to datD" << endl;
                        }
                    }
                    if (datD.size() > 0){
                        csvOut.data[csvOut.size()-1][keyPos] = to_string(mean(datD));
                        cout << "combineMultipleEntries: csvOut.data[" << csvOut.size()-1 << "][" << keyPos << "] set to <" << csvOut.data[csvOut.size()-1][keyPos] << ">" << endl;
                    }
                }
            }
            done.push_back((*it)[pos]);

            ///write data
            outStr = csvOut.data[csvOut.size()-1][0];
            for (int i=1; i<csvOut.data[csvOut.size()-1].size(); i++){
                outStr += ","+csvOut.data[csvOut.size()-1][i];
            }
            outStr += "\n";
            myfile << outStr;
        }
    }

    myfile.close();
    return csvOut;
}


void CSVData::printHeader() const{
    cout << header[0];
    for (int i=1; i<header.size(); ++i)
        cout << ", " << header[i];
    cout << endl;
}

vector<string> split(string const& str, string const& delimiter){
    vector<string> elems;
    size_t pos = 0;
    string token;
    string s(str);
    size_t nTokens = 0;
    while ((pos = s.find(delimiter)) != string::npos){
        token = s.substr(0,pos);
//        cout << "split: token " << nTokens << " = <" << token << ">" << endl;
        elems.push_back(token);
        s.erase(0,pos+delimiter.length());
        ++nTokens;
//        cout << s << ".find(" << delimiter << ") = " << s.find(delimiter) << endl;
    }
//    cout << "s = <" << s << ">" << endl;
    elems.push_back(s);
    return elems;
}

vector<string> readHeader(string const& fileName, string const& delimiter){
    ifstream inStream(fileName);
    vector<string> header;
    string line;
    if (getline(inStream, line)){
        header = split(line, delimiter);
        cout << "header.size() = " << header.size() << endl;
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
//    cout << "writeStrVecToFile: wrote line <" << strToWrite << "> to outFile" << endl;
    return;
}

int countCommasInLine(string const& line){
    char delimiter = ',';
    return count(line.begin(), line.end(), delimiter);
}

int countCommas(string const& fileName){
    ifstream inStream(fileName);
    string line;
    int nCommas = 0;
    int nCommasLast=0;
    int iLine = 0;
    while (getline(inStream, line)){
        nCommas = countCommasInLine(line);
        cout << "csvData::countCommas: nCommas = " << nCommas << endl;
        if ((iLine > 0) && (nCommas != nCommasLast)){
            cout << "csvData: count Commas: ERROR: nCommasLast(=" << nCommasLast << ") != nCommas(=" << nCommas << ")" << endl;
        }
        nCommasLast = nCommas;
        iLine += 1;
    }
//    nCommas = count(substring.begin(), substring.end(), ',');
    return nCommas;
}

CSVData readCSVFile(string const& fileName, string const& delimiter, bool const& removeBadLines){
    ifstream inStream(fileName);
    if (!inStream.is_open()){
        cout << "file with name <" << fileName << "> is not open" << endl;
        exit(EXIT_FAILURE);
    }
    int nBadLines = 0;
    CSVData csvData;
    struct timeval start, end;

    gettimeofday(&start, NULL);

    if (inStream.is_open()){
        int iLine = 0;
        string line, previousLine;
        while (getline(inStream, line)){
            int nCommas = 0;
            int nQuotes = count(line.begin(), line.end(), '"');
            while (!isEven(nQuotes)){
                string newLine;
                getline(inStream, newLine);
                line += newLine;
                nQuotes = count(line.begin(), line.end(), '"');
//                throw std::runtime_error("found uneven number of quotes ("+to_string(nQuotes)+") in line <"+line+">");
            }
            line = replaceDelimiterInsideQuotes(line, delimiter);
            string lineSplit(line);
///            if (nQuotes > 0){
///                vector<string> quotes = split(lineSplit,"\"");
///                for (size_t iS=0; iS<quotes.size(); ++iS)
///                    nCommas += split(quotes[iS], ",").size();
///            }
///            else
            vector<string> elems = split(lineSplit,delimiter);
            for (auto itElem=elems.begin(); itElem!=elems.end(); ++itElem)
                stripUnicode(*itElem);
            nCommas = elems.size()-1;//count(line.begin(), line.end(), delimiter);
            //cout << "line contains " << nCommas << " commas" << endl;
            lineSplit = line;
            if (iLine == 0){
                csvData.header = elems;
                iLine = 1;
                previousLine = line;
                cout << "readCSVFile: " << fileName << " contains " << csvData.header.size() << " columns" << endl;
                continue;
            }
            if (nCommas != csvData.header.size()-1){
                if (removeBadLines){
                    cout << "readCSVFile: " << fileName << ": ERROR: nCommas = " << nCommas << " != csvData.header.size()-1 = " << csvData.header.size()-1 << endl;
                    cout << "previousLine = " << previousLine << ": " << count(previousLine.begin(), previousLine.end(), delimiter.c_str()[0]) << " commas" << endl;
                    cout << "line = " << line << ": " << count(line.begin(), line.end(), delimiter.c_str()[0]) << " commas" << endl;
                    int iStop = nCommas > csvData.header.size() ? nCommas : csvData.header.size();
                    for (int k=0; k<=iStop; ++k){
                        if (k < csvData.header.size())
                            cout << "header[" << k << "] = " << csvData.header[k] << ": ";
                        if (k < elems.size())
                            cout << "data = " << elems[k];
                        if (csvData.size() > 0)
                            if (k < csvData.data[csvData.size()-1].size())
                            cout << ": previous data = " << csvData.data[csvData.size()-1][k];
                        cout << endl;
                    }
                }
                nBadLines++;
                if (!removeBadLines){
                    vector<string> dataLine(elems);
                    csvData.data.push_back(dataLine);
                    previousLine = line;
//                    exit(EXIT_FAILURE);
                }
            }
            else{
                vector<string> dataLine(elems);
//                lineSplit = line;
//                if (nQuotes > 0){
//                    vector<string> quotes = split(lineSplit,"\"");
//                    for (size_t iS=0; iS<quotes.size(); ++iS){
//                        vector<string> dataLineTemp = split(quotes[iS], to_string(delimiter));
//                        for (size_t iD=0; iD<dataLineTemp.size(); ++iD)
//                            dataLine.push_back(dataLineTemp[iD]);
//                    }
//                }
//                else{
//                    dataLine = split(lineSplit,to_string(delimiter));
//                }
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

CSVData readCSVFile(string const& fileName){
    return readCSVFile(fileName, ",", true);
}

void writeCSVFile(CSVData const& dat, string const& fileName){
    std::ofstream myfile;
    myfile.open(fileName);

    ///write header
    string outStr = dat.header[0];
    for (int i=1; i<dat.header.size(); i++){
        outStr += ","+dat.header[i];
    }
    outStr += "\n";
    myfile << outStr;

    ///write data
    for (int iLine = 0; iLine < dat.size(); ++iLine){
        vector<string> data = dat.getData(iLine);
        outStr = data[0];
        for (int i=1; i<data.size(); i++){
            outStr += ","+data[i];
        }
        outStr += "\n";
        myfile << outStr;
    }

    myfile.close();
    return;
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

vector<string> splitCSVLine(string const& line, char const& delimiter){
    string tmpStr(line);
    cout << "splitCSVLine: tmpStr = " << tmpStr << endl;
    vector<string> out(0);
    size_t kommaPos = tmpStr.find(to_string(delimiter));
    cout << "splitCSVLine: kommaPos = " << kommaPos << endl;
    while (kommaPos != string::npos){
        out.push_back(tmpStr.substr(0,kommaPos));
        tmpStr = tmpStr.substr(kommaPos+1);
        cout << "splitCSVLine: tmpStr = " << tmpStr << endl;
        kommaPos = tmpStr.find(to_string(delimiter));
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

CSVData crossMatch(CSVData const& csvDataA, CSVData const& csvDataB, string const& key){
    CSVData csvDataOut;
    vector<string> headerA = csvDataA.header;
    vector<string> headerB = csvDataB.header;
    for (size_t iHeader=0; iHeader<headerA.size(); iHeader++){
        csvDataOut.header.push_back(headerA[iHeader]);
//        cout << "crossMatch: added headerA[" << iHeader << "] = <" << headerA[iHeader] << "> to csvDataOut" << endl;
//        cout << "crossMatch: csvDataOut.header[" << csvDataOut.header.size()-1 << "] = " << csvDataOut.header[csvDataOut.header.size()-1] << endl;
    }
    for (size_t iHeader=0; iHeader<headerB.size(); iHeader++){
//        cout << "crossMatch: csvDataOut.header.size() = " << csvDataOut.header.size() << endl;
        auto pos = std::find(csvDataOut.header.begin(), csvDataOut.header.end(), headerB[iHeader]);
        if (pos == csvDataOut.header.end()){
            csvDataOut.header.push_back(headerB[iHeader]);
//            cout << "crossMatch: added headerB[" << iHeader << "] = <" << headerB[iHeader] << "> to csvDataOut" << endl;
//            cout << "crossMatch: csvDataOut.header[" << csvDataOut.header.size()-1 << "] = " << csvDataOut.header[csvDataOut.header.size()-1] << endl;
        }
//        else{
//            cout << "crossMatch: found headerB[" << iHeader << "] = <" << headerB[iHeader] << "> in csvDataOut at position " << pos - csvDataOut.header.begin() << endl;
//        }
    }

    string valA;
    size_t lenA = csvDataA.size();
    size_t lenB = csvDataB.size();
    vector<string> lineOut(csvDataOut.header.size());
    vector<string> valsB = csvDataB.getData(key);
    for (size_t iA=0; iA<lenA; ++iA){
//        cout << "crossMatch: searching for star number " << iA << " out of " << lenA << " stars in data set A" << endl;
        valA = csvDataA.getData(key, iA);
        size_t iB = std::find(valsB.begin(), valsB.end(), valA) - valsB.begin();
        cout << "crossMatch: iB = " << iB << ", valsB.size() = " << valsB.size() << ", iB = " << iB << endl;
        if (iB != valsB.size()){
            cout << "crossMatch: found <" << valA << "> in data set B at position " << to_string(iB) << endl;
            for (size_t iHeader=0; iHeader<headerA.size(); ++iHeader){
                lineOut[csvDataOut.findKeywordPos(headerA[iHeader])] = csvDataA.getData(headerA[iHeader], iA);
            }
            for (size_t iHeader=0; iHeader<headerB.size(); ++iHeader){
                lineOut[csvDataOut.findKeywordPos(headerB[iHeader])] = csvDataB.getData(headerB[iHeader], iB);
            }
            csvDataOut.data.push_back(lineOut);
        }
        else{
            cout << "crossMatch: could not find <" << valA << "> in data set B" << endl;
        }
    }
    cout << "crossMatch: found" << csvDataOut.data.size() << " stars" << endl;
    return csvDataOut;
}

/*vector<double> getGaiaG(CSVData const& csvData){
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
}*/

bool isEven(int n){
    return (n % 2 == 0);
}

template < typename T >
std::pair<bool, int> findInVector(const std::vector<T> & vecOfElements, const T& element){
    std::pair<bool, int> result;
    auto it = std::find(vecOfElements.begin(), vecOfElements.end(), element);
    if (it != vecOfElements.end()){
        result.second = distance(vecOfElements.begin(), it);
        result.first = true;
    }
    else{
        result.first = false;
        result.second = -1;
    }
    return result;
}
template std::pair<bool, int> findInVector(const std::vector<string> &, const string &);

double mean(vector< double > const& valVec){
    double sum = std::accumulate(valVec.begin(), valVec.end(), 0.0);
    return sum / valVec.size();
}

string replaceDelimiterInsideQuotes(const string& line, const string& delimiter){
    int nQuotes = count(line.begin(), line.end(), '"');
    if (!isEven(nQuotes)){
        throw std::runtime_error("replaceDelimiterInsideQuotes: found uneven number of quotes in line <"+line+">");
    }
    string lineOut;
    string delimiterReplacement = ";";
    if (delimiter.compare(";") == 0)
        delimiterReplacement = ",";
    if (nQuotes > 0){
        string lineSplit(line);
        while(count(lineSplit.begin(), lineSplit.end(),'"') > 0){
            lineOut += lineSplit.substr(0,lineSplit.find('"'));
            lineSplit = lineSplit.substr(lineSplit.find('"')+1,lineSplit.length());
            string insideQuotes = lineSplit.substr(0,lineSplit.find('"'));
            while(insideQuotes.find(delimiter) != string::npos)
                insideQuotes.replace(insideQuotes.find(delimiter), strlen(delimiter.c_str()), delimiterReplacement);
            lineOut += insideQuotes;
            lineSplit = lineSplit.substr(lineSplit.find('"')+1,lineSplit.length());
        }
        lineOut += lineSplit;
    }
    else{
        lineOut = line;
    }
    return lineOut;
}

bool invalidChar (char c)
{
    return !(c>=0 && c <128);
}
void stripUnicode(string & str)
{
    str.erase(remove_if(str.begin(),str.end(), invalidChar), str.end());
}