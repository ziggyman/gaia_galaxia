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
                string const& outFileName){
    string galaxiaFileName = galaxiaGetDataDirOut()
                             + (galaxiaGetFileNameOutRoot() % pixels[pixelId].xLow
                                                            % pixels[pixelId].xHigh
                                                            % pixels[pixelId].yLow
                                                            % pixels[pixelId].yHigh).str();
    string gaiaFileName = gaiaGetDataDirOut()
                          + (gaiaGetFileNameOutRoot() % pixels[pixelId].xLow
                                                      % pixels[pixelId].xHigh
                                                      % pixels[pixelId].yLow
                                                      % pixels[pixelId].yHigh).str();

    unsigned nStarsGaia = countLines(gaiaFileName);
    unsigned nStarsGalaxia = countLines(galaxiaFileName);
    string lockName = "/var/lock/out.lock";
    int fd = lockFile(outFileName,
                      lockName,
                      0.1);
    ofstream outFile(outFileName, ios_base::app);

    string strToWrite = to_string(pixelId) + " " + to_string(nStarsGalaxia) + " " + to_string(nStarsGaia);
    outFile.write(strToWrite.c_str(), strlen(strToWrite.c_str()));
    string endOfLine("\n");
    outFile.write(endOfLine.c_str(), strlen(endOfLine.c_str()));
    closeFileAndDeleteLock(outFile,
                           lockName,
                           fd);
}

vector< vector< string > > getGaiaObject(CSVData const& csvData, string const& source_id){
    int nDataLines = csvData.data.size();
    cout << "csvData has " << nDataLines << " data lines" << endl;

    vector<string> sourceIds = csvData.getData("source_id");
    vector< vector< string > > out(0);
    for (int pos=0; pos!=sourceIds.size(); ++pos){
        if (sourceIds[pos].compare(source_id) == 0){
            out.push_back(csvData.data[pos]);
        }
    }
    return out;
}
