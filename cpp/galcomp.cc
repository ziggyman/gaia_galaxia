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

string getCSVFileName(Pixel const& pixel, string const& whichOne){
    string fName;
    if (whichOne.compare("galaxia") == 0){
        fName = galaxiaGetDataDirOut() +
                (galaxiaGetFileNameOutRoot() % pixel.xLow
                                             % pixel.xHigh
                                             % pixel.yLow
                                             % pixel.yHigh).str();
    }
    else if (whichOne.compare("gaia") == 0){
        fName = gaiaGetDataDirOut() +
                (gaiaGetFileNameOutRoot() % pixel.xLow
                                          % pixel.xHigh
                                          % pixel.yLow
                                          % pixel.yHigh).str();
    }
    else if (whichOne.compare("gaiaTgas") == 0){
        fName = gaiaTgasGetDataDirOut() +
                (gaiaTgasGetFileNameOutRoot() % pixel.xLow
                                              % pixel.xHigh
                                              % pixel.yLow
                                              % pixel.yHigh).str();
    }
    else{
        throw std::runtime_error("ERROR: whichOne(=<"+whichOne
                +"> not found in possible options [galaxia, gaia, gaiaTgas]");
    }

}

vector<string> getHeader(string const& whichOne){
    Hammer hammer();
    Pixel pix = hammer.getPixels()[0];
    return readHeader(getCSVFileName(pix, whichOne));
}

vector<Pixel> getPixelsInXYWindow(vector<Pixel> const& pixelsIn, Pixel const& windowIn){
    vector<Pixel> out(0);
    for (auto itPix=pixelsIn.begin(); itPix!=pixelsIn.end(); ++itPix){
        if (windowIn.isInside(XY(itPix->xLow, itPix->yLow))
         || windowIn.isInside(XY(itPix->xHigh, itPix->yLow))
         || windowIn.isInside(XY(itPix->xLow, itPix->yHigh))
         || windowIn.isInside(XY(itPix->xHigh, itPix->yHigh))){
            out.push_back(*itPix);
        }
    }
    return out;
}

CSVData getStarsInXYWindow(vector<Pixel> const& pixelsIn, Pixel const& window, string const& whichOne){
    vector<Pixel> goodPixels = getPixelsInXYWindow(pixelsIn, window);

    CSVData csvDataOut;
    csvDataOut._header = getHeader(whichOne);
    Hammer hammer;
    int headerPosX = csvDataOut.findKeywordPos(hammer.getKeyWordHammerX());
    int headerPosXY= csvDataOut.findKeywordPos(hammer.getKeyWordHammerX());
    for (auto itPix=goodPixels.begin(); itPix!=goodPixels.end(); ++itPix){
        string fName = getCSVFileName(*itPix, whichOne);
        CSVDataIn csvDataIn = readCSVFile(fName);
        for (auto itStar=csvDataIn._data.begin(); itStar!=csvDataIn._data.end(); ++itStar){
            if (itPix->isInside(XY((*itStar)[headerPosX], (*itStar)[headerPosY]))){
                csvDataOut._data.push_back(*itStar);
            }
        }
    }
    return csvDataOut;
}

void simulateObservation(Pixel const& xyWindow, string const& filter, string const& whichObs){
    Hammer hammer;
    vector<Pixel> pixels = hammer.getPixels()

    CSVData csvDataObs = getStarsInXYWindow(pixels, xyWindow, whichObs);
    CSVData csvDataModel = getStarsInXYWindow(pixels, xyWindow, "galaxia");

    vector<double> appMagFilterObs = convertStringVectorToDoubleVector(
        csvDataObs.getData(gaiaGetFilterKeyWord(filter)));
    vector<double> appMagFilterModel = convertStringVectorToDoubleVector(
        csvDataModel.getData(galaxiaGetFilterKeyWord(filter)));

    
}

void comparePixel(Pixel const& xyWindow, string const& keyWord, string const& whichObs){

}
