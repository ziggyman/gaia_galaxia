#include "galcomp.h"

int existsHowManyTimes(vector<string> const& inVec, string const& in){
    int nTimes(0);
    for (auto it=inVec.begin(); it!=inVec.end(); ++it){
        if (it->compare(in) == 0)
            ++nTimes;
    }
    return nTimes;
}

void countStars(vector<Pixel> const& pixels,
                int const& pixelId,
                string const& outFileName,
                string const& whichOne){
    string inFileName;

    if (whichOne.compare("galaxia") == 0){
        inFileName = galaxiaGetDataDirOut()
                             + (galaxiaGetFileNameOutRoot() % pixels[pixelId].xLow
                                                            % pixels[pixelId].xHigh
                                                            % pixels[pixelId].yLow
                                                            % pixels[pixelId].yHigh).str();
    }
    else if (whichOne.compare("gaia") == 0){
        inFileName = gaiaGetDataDirOut()
                        + (gaiaGetFileNameOutRoot() % pixels[pixelId].xLow
                                                    % pixels[pixelId].xHigh
                                                    % pixels[pixelId].yLow
                                                    % pixels[pixelId].yHigh).str();
    }
    else if (whichOne.compare("gaiaTgas") == 0){
        inFileName = gaiaTgasGetDataDirOut()
                        + (gaiaTgasGetFileNameOutRoot() % pixels[pixelId].xLow
                                                        % pixels[pixelId].xHigh
                                                        % pixels[pixelId].yLow
                                                        % pixels[pixelId].yHigh).str();
    }
    else{
        throw std::runtime_error("countStars: whichOne = <"+whichOne+"> not found in [gaia, gaiaTgas]");
    }
    unsigned nStars = countLines(inFileName);
    string lockName = "/var/lock/"+outFileName.substr(outFileName.find_last_of("/")+1)+".lock";
    int fd = lockFile(outFileName,
                      lockName,
                      0.1);
    ofstream outFile(outFileName, ios_base::app);

    string strToWrite = to_string(pixelId) + "," + to_string(nStars)+"\n";
    outFile.write(strToWrite.c_str(), strlen(strToWrite.c_str()));
    closeFileAndDeleteLock(outFile,
                           lockName,
                           fd);
}

vector< vector< string > > getGaiaObject(CSVData const& csvData, string const& source_id){
    int nDataLines = csvData._data.size();
    cout << "csvData has " << nDataLines << " data lines" << endl;

    vector<string> sourceIds = csvData.getData("source_id");
    vector< vector< string > > out(0);
    for (int pos=0; pos!=sourceIds.size(); ++pos){
        if (sourceIds[pos].compare(source_id) == 0){
            out.push_back(csvData._data[pos]);
        }
    }
    return out;
}
