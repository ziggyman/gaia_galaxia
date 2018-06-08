#include "galcomp.h"
#include "math.h"

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
        inFileName = modelGetDataDirOut()
                             + (modelGetFileNameOutRoot() % pixels[pixelId].xLow
                                                          % pixels[pixelId].xHigh
                                                          % pixels[pixelId].yLow
                                                          % pixels[pixelId].yHigh).str();
    }
    else if ((whichOne.compare("gaia") == 0) || (whichOne.compare("gaiaTgas") == 0)){
        inFileName = obsGetDataDirOut(whichOne)
                        + (obsGetFileNameOutRoot(whichOne) % pixels[pixelId].xLow
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

string getCSVFileName(Pixel const& pixel, string const& whichOne){
    string fName;
    if (whichOne.compare("galaxia") == 0){
        fName = modelGetDataDirOut() +
                (modelGetFileNameOutRoot() % pixel.xLow
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
    return fName;
}

vector<string> getHeader(string const& whichOne){
    Hammer hammer;
    Pixel pix = hammer.getPixels()[0];
    return readHeader(getCSVFileName(pix, whichOne));
}

vector<Pixel> getPixelsInXYWindow(vector<Pixel> const& pixelsIn, Pixel const& windowIn){
    vector<Pixel> out(0);
    double tmp = 0.000000001;
    for (auto itPix=pixelsIn.begin(); itPix!=pixelsIn.end(); ++itPix){
        if (windowIn.isInside(XY(itPix->xLow + tmp, itPix->yLow + tmp))
         || windowIn.isInside(XY(itPix->xHigh - tmp, itPix->yLow + tmp))
         || windowIn.isInside(XY(itPix->xLow + tmp, itPix->yHigh - tmp))
         || windowIn.isInside(XY(itPix->xHigh - tmp, itPix->yHigh - tmp))
         || itPix->isInside(XY(windowIn.xLow, windowIn.yLow))
         || itPix->isInside(XY(windowIn.xLow, windowIn.yHigh))
         || itPix->isInside(XY(windowIn.xHigh, windowIn.yLow))
         || itPix->isInside(XY(windowIn.xHigh, windowIn.yHigh))){
            out.push_back(*itPix);
        }
    }
    return out;
}

CSVData getStarsInXYWindow(vector<Pixel> const& pixelsIn, Pixel const& window, string const& whichOne){
    cout << "getStarsInXYWindow: whichOne = " << whichOne << endl;
    cout << "getStarsInXYWindow: xindow = [" << window.xLow << ", " << window.xHigh << "; " << window.yLow << ", " << window.yHigh << "]" << endl;
    if (window.xLow >= window.xHigh)
        throw std::runtime_error("getStarsInXYWindow: ERROR: xLow >= xHigh");
    if (window.yLow >= window.yHigh)
        throw std::runtime_error("getStarsInXYWindow: ERROR: yLow >= yHigh");

    vector<Pixel> goodPixels = getPixelsInXYWindow(pixelsIn, window);
    cout << "getStarsInXYWindow: goodPixels = " << goodPixels.size() << ": ";
    for (Pixel& pix: goodPixels) cout << "[" << pix.xLow << ", " << pix.xHigh << "; " << pix.yLow << ", " << pix.yHigh << "] ";
    cout << endl;

    CSVData csvDataOut;
    csvDataOut.header = getHeader(whichOne);
    cout << "getStarsInXYWindow: csvDataOut.header = ";
    for (string& str: csvDataOut.header) cout << str << ", ";
    cout << endl;
    Hammer hammer;
    int headerPosX = csvDataOut.findKeywordPos(hammer.getKeyWordHammerX());
    int headerPosY= csvDataOut.findKeywordPos(hammer.getKeyWordHammerY());
    for (auto itPix=goodPixels.begin(); itPix!=goodPixels.end(); ++itPix){
        string fName = getCSVFileName(*itPix, whichOne);
        cout << "getStarsInXYWindow: fName = <" << fName << ">" << endl;
        CSVData csvDataIn = readCSVFile(fName);
        cout << "getStarsInXYWindow: csvDataIn.size() = " << csvDataIn.size() << endl;
        for (auto itStar=csvDataIn.data.begin(); itStar!=csvDataIn.data.end(); ++itStar){
            if (window.isInside(XY(stod((*itStar)[headerPosX]), stod((*itStar)[headerPosY])))){
                csvDataOut.data.push_back(*itStar);
//                cout << "getStarsInXYWindow: star found at [x=" << (*itStar)[headerPosX] << ", y=" << (*itStar)[headerPosY] << "]" << endl;
            }
//            else
//                cout << "getStarsInXYWindow: star at [x=" << (*itStar)[headerPosX] << ", y=" << (*itStar)[headerPosY] << "] outside window [" << window.xLow << ", " << window.xHigh << "; " << window.yLow << ", " << window.yHigh << "]" << endl;
        }
    }
    cout << "getStarsInXYWindow: csvDataOut.size() = " << csvDataOut.size() << endl;
    return csvDataOut;
}

vector< vector< vector< unsigned > > > simulateObservation(
    vector<Pixel> const& pixels,
    Pixel const& xyWindow,
    string const& filter,
    string const& whichObs,
    unsigned nSims)
{
    CSVData csvDataObs = getStarsInXYWindow(pixels, xyWindow, whichObs);
    cout << "simluateObservation: csvDataObs.size() = " << csvDataObs.size() << endl;
    CSVData csvDataModel = getStarsInXYWindow(pixels, xyWindow, "galaxia");
    cout << "simluateObservation: csvDataModel.size() = " << csvDataModel.size() << endl;

//    string filterKeyWordObs = gaiaGetFilterKeyWord(filter);
//    cout << "simulateObservation: filterKeyWordObs = <" << filterKeyWordObs << ">" << endl;
//    vector<string> appMagFilterObsStr = csvDataObs.getData(filterKeyWordObs);
//    cout << "simulateObservation: appMagFilterObsStr.size() = " << appMagFilterObsStr.size() << endl;
    vector<double> appMagFilterObs = convertStringVectorToDoubleVector(
        csvDataObs.getData(obsGetFilterKeyWord(filter)));
    cout << "simluateObservation: appMagFilterObs.size() = " << appMagFilterObs.size() << endl;

    vector<double> appMagFilterModel = getGaiaG(csvDataModel);
    cout << "simluateObservation: appMagFilterModel.size() = " << appMagFilterModel.size() << endl;
//    for (double& x: appMagFilterModel) cout << x << ", ";
//    cout << endl;

    if (appMagFilterObs.size() == 0)
        throw std::runtime_error("simulateObservation: ERROR: no stars in appMagFilterObs");

    Histogram obsHist;
    double minMagObs = *min_element(appMagFilterObs.begin(), appMagFilterObs.end());
    double maxMagObs = *max_element(appMagFilterObs.begin(), appMagFilterObs.end());
    cout << "simluateObservation: minMagObs = " << minMagObs << endl;
    cout << "simluateObservation: maxMagObs = " << maxMagObs << endl;

    obsHist.makeBinLimits(minMagObs, maxMagObs, getNStepsMagnitude());
    for (pair<double, double>& lim: obsHist.limits) cout << "limit = [" << lim.first << ", " << lim.second << ")" << endl;
    obsHist.make(appMagFilterObs);
    cout << "simulateObservation: obsHist.indices.size()" << obsHist.indices.size() << endl;
    for (int i=0; i<obsHist.indices.size(); ++i)
        cout << "simulateObservation: obsHist.indices[" << i << "].size()" << obsHist.indices[i].size() << endl;

    vector< vector< vector< unsigned > > > sims(0);
    sims.push_back(obsHist.indices);
    cout << "simulateObservation: sims.size() = " << sims.size() << endl;
    unsigned seed = 1;
    for (unsigned sim=0; sim < nSims; ++sim){
        cout << "simulateObservation: iSim = " << sim << ", seed = " << seed << endl;
        sims.push_back(obsHist.fillRandomly(appMagFilterModel, seed));
        cout << "simulateObservation: seed = " << seed << endl;
    }
    return sims;
}

void comparePixel(vector<Pixel> const& pixels,
                  Pixel const& xyWindow,
                  string const& keyWord,
                  string const& whichObs){
    vector< vector< vector< unsigned > > > data = simulateObservation(pixels,
                                                                      xyWindow,
                                                                      obsGetFilter(),
                                                                      whichObs,
                                                                      getNSims());
    cout << "comparePixel: getNSims() = " << getNSims() << ": data.size() = " << data.size() << endl;
    /// more to follow once this works
}

vector< pair< float, float > > getHistogramLimits(int const& nBars,
                                                  float const& xMin,
                                                  float const& xMax){
    vector< pair< float, float > > limits(nBars);
    float dist = (xMax - xMin) / float(nBars);
    limits[0].first = xMin;
    limits[0].second = xMin + dist;
    for (int i = 1; i < nBars; ++i){
        limits[i].first = limits[i-1].second;
        limits[i].second = limits[i].first + dist;
    }
    cout << "makeHistogram: xMin = " << xMin << ", limits[0].first = " << limits[0].first << endl;
    cout << "makeHistogram: xMax = " << xMax << ", limits[" << nBars - 1 << "].second = " << limits[nBars-1].second << endl;
    return limits;
}
/*
string getHeaderKeyWord(string const& keyWord,
                        string const& whichOne){
    if ((whichOne.compare("gaia") == 0) or (whichOne.compare("gaiaTgas") == 0))
        return obsGetHeaderKeyWord(keyWord);
    else if (whichOne.compare("galaxia") == 0)
        return modelGetHeaderKeyWord(keyWord);
    else
        throw std::runtime_error("getHeaderKeyWord: ERROR: whichOne = <"+whichOne+"> not recognized");
}

vector<int> getHistogram(vector<Pixel> const& pixelsIn,
                         Pixel const& xyWindow,
                         string const& whichOne,
                         string const& keyWord,
                         vector< pair< float, float > > limits){
    /// get stars in xyWindow
    CSVData stars = getStarsInXYWindow(pixelsIn,
                                       xyWindow,
                                       whichOne);

    string headerKeyWord = getHeaderKeyWord(keyWord, whichOne);

    vector<float> data;
    if (headerKeyWord.compare("G") == 0){
        if ((whichOne.compare("gaia") == 0) or (whichOne.compare("gaiaTgas") == 0))
            data = stars.getData(headerKeyWord);
        else
            data = getGaiaG(stars);
    }
    else
        data = stars.getData(headerKeyWord);

    vector<int> histogram(limits.size(), int(0));

    for (auto it = data.begin(); it != data.end(); ++it){
        auto itHist = histogram.begin();
        for (auto itLim = limits.begin(); itLim != limits.end(); ++itLim, ++itHist){
            if ((*it >= itLim->first) && (*it < itLim->second)){
                *itHist += 1;
                break;
            }
        }
    }

    return histogram;
}

void makeHistogram(vector<Pixel> const& pixelsIn,
                   Pixel const& xyWindow,
                   vector<string> const& whichOnes,
                   string const& keyWord,
                   vector< pair< float, float > > limits,
                   string const& outFileName){
    /// get all stars in xyWindow for each string in whichOne
    vector< vector< int > > histograms(whichOnes.size());
    auto itWhichOne = whichOnes.begin();
    for (auto itHist = histograms.begin(); itHist != histograms.end(); ++itHist, ++itWhichOne){
        *itHist = getHistogram(pixelsIn,
                               xyWindow
                               *itWhichOne,
                               keyWord,
                               limits);
    }



}
*/