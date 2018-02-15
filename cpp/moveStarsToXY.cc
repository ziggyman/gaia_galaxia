#include "moveStarsToXY.h"

vector<string> galaxiaGetInputFileNames(){
    string dataDir("/Volumes/yoda/azuri/data/galaxia/lon-lat/");
    boost::format fileNameRoot = boost::format("galaxia_%i-%i_%i-%i.csv");// % (int(minLongitude), int(maxLongitude), int(minLatitude), int(maxLatitude))
    vector<string> inputFileNames(0);
    for (int lon=-80; lon<=180; lon+=10){
        for (int lat=-80; lat<=90; lat+=10){
            inputFileNames.push_back(dataDir + (fileNameRoot % (lon-10)
                                                             % lon
                                                             % (lat-10)
                                                             % lat).str());
        }
    }
    return inputFileNames;
}

vector<string> gaiaGetInputFileNames(){
    string dataDir("/Volumes/external/azuri/data/gaia/cdn.gea.esac.esa.int/Gaia/gaia_source/csv/");
    boost::format fileNameRoot = boost::format("GaiaSource_%03i-%03i-%03i.csv");//% (release, tract, patch);
    vector<string> inputFileNames(0);
    for (int iRelease=0; iRelease<3; ++iRelease){
        for (int iTract=0; iTract<1000; ++iTract){
            for (int iPatch=0; iPatch<1000; ++iPatch){
                std::string fileName = dataDir + (fileNameRoot % iRelease
                                                               % iTract
                                                               % iPatch).str();
                if (ifstream(fileName)){/// File exists
                    inputFileNames.push_back(fileName);
                }
            }
        }
    }
    return inputFileNames;
}

vector<string> gaiaTgasGetInputFileNames(){
    string dataDir("/Volumes/yoda/azuri/data/gaia-tgas/");
    boost::format fileNameRoot = boost::format("TgasSource_%03i-%03i-%03i.csv");//% (release, tract, patch);
    vector<string> inputFileNames(0);
    for (int iRelease=0; iRelease<1; ++iRelease){
        for (int iTract=0; iTract<1; ++iTract){
            for (int iPatch=0; iPatch<16; ++iPatch){
                std::string fileName = dataDir + (fileNameRoot % iRelease
                                                               % iTract
                                                               % iPatch).str();
                if (ifstream(fileName)){/// File exists
                    inputFileNames.push_back(fileName);
                }
            }
        }
    }
    return inputFileNames;
}

vector<string> gaiaGetInputFileNamesFromLonLat(){
    string dataDir("/Volumes/external/azuri/data/gaia/lon-lat/");
    boost::format fileNameRoot = boost::format("GaiaSource_%i-%i_%i-%i.csv");// % (int(minLongitude), int(maxLongitude), int(minLatitude), int(maxLatitude))
    vector<string> inputFileNames(0);
    for (int lon=10; lon<=360; lon+=10){
        for (int lat=-80; lat<=90; lat+=10){
            inputFileNames.push_back(dataDir + (fileNameRoot % (lon-10)
                                                             % lon
                                                             % (lat-10)
                                                             % lat).str());
        }
    }
    return inputFileNames;
}

vector< std::shared_ptr< ofstream > > getOutFiles(vector<Pixel> const& pixels){
    int nPix = pixels.size();

    vector< std::shared_ptr< ofstream > > outFiles(0);
    outFiles.reserve(nPix);
    for (int iPix=0; iPix<nPix; ++iPix){
        std::shared_ptr<ofstream> outFile(new ofstream);
        outFiles.push_back(outFile);
    }
    return outFiles;
}

vector<string> getOutFileNames(vector<Pixel> const& pixels,
                               string const& whichOne){
    vector<string> outFileNames(0);
    boost::format fileNameOutRoot;
    string dataDirOut;
    if (whichOne.compare("galaxia") == 0){
        fileNameOutRoot = modelGetFileNameOutRoot();
        dataDirOut = modelGetDataDirOut();
    }
    else if (whichOne.compare("gaia") == 0){
        fileNameOutRoot = gaiaGetFileNameOutRoot();
        dataDirOut = gaiaGetDataDirOut();
    }
    else if (whichOne.compare("gaiaTgas") == 0){
        fileNameOutRoot = gaiaTgasGetFileNameOutRoot();
        dataDirOut = gaiaTgasGetDataDirOut();
    }
    else{
        cout << "getOutFileNames: ERROR: whichOne(=<" << whichOne << ">) neither equal to <galaxia> nor to <gaia> nor to <gaiaTgas>" << endl;
        exit(EXIT_FAILURE);
    }
    outFileNames.reserve(pixels.size());
    for (int iPix=0; iPix<pixels.size(); ++iPix){
        string outFileName = dataDirOut + (fileNameOutRoot % pixels[iPix].xLow
                                                           % pixels[iPix].xHigh
                                                           % pixels[iPix].yLow
                                                           % pixels[iPix].yHigh).str();
        outFileNames.push_back(outFileName);
    }
    return outFileNames;
}

void writeHeaderToOutFiles(vector<string> const& header,
                           vector<Pixel> const& pixels,
                           string const& whichOne,
                           bool const& append){
    cout << "opening outfiles and writing headers" << endl;
    vector<string> outFileNames = getOutFileNames(pixels, whichOne);
    vector< std::shared_ptr< ofstream > > outFiles = getOutFiles(pixels);
    for (int i=0; i<outFiles.size(); ++i){
        outFiles[i]->exceptions(ofstream::failbit | ofstream::badbit);
        if (!append || !ifstream(outFileNames[i])){
            cout << "writing outFile <" << outFileNames[i] << "> because append==false or it does not exist yet" << endl;
            outFiles[i]->open(outFileNames[i]);
            writeStrVecToFile(header, *outFiles[i]);
            outFiles[i]->close();
        }
    }
    return;
}

void gaiaMoveStarsToXY(){
    moveStarsToXY("gaia");
}

void gaiaTgasMoveStarsToXY(){
    moveStarsToXY("gaiaTgas");
}

void gaiaMoveStarsFromLonLatToXY(){
    moveStarsToXY("gaiaFromLonLat");
}

void galaxiaMoveStarsFromLonLatToXY(){
    moveStarsToXY("galaxia");
}

void appendCSVDataToXYFiles(CSVData const& csvData,
                            vector<Pixel> const& pixels,
                            string const& whichOne,
                            vector<string> const& ids,
                            bool const& doFind,
                            string const& lockSuffix){
    bool doWrite = true;
    Hammer ham;

    vector< std::shared_ptr< ofstream > > const& outFiles = getOutFiles(pixels);
    vector<string> const& outFileNames = getOutFileNames(pixels, whichOne);
    cout << "moveStarsToXY.appendCSVDataToXYFiles: outFileNames[0] = " << outFileNames[0] << endl;

    vector< string > locks(0);
    vector< int > lockFds(0);
    vector< std::shared_ptr< ofstream > > filesOpened(0);
    locks.reserve(1000);
    lockFds.reserve(1000);
    filesOpened.reserve(1000);

    time_t start, end;
    time_t findsStart, findsEnd;
    time (&start); // note time before execution

    int nStarsWritten = 0;
    bool lastEntryFound = true;
    bool alreadyThere = false;
    vector<bool> starFoundInIds(ids.size());
    if (doFind){
        time (&findsStart); // note time before execution
    }

    string keyWordHammerX = ham.getKeyWordHammerX();
    string keyWordHammerY = ham.getKeyWordHammerY();
    for (int iStar=0; iStar<csvData.size(); ++iStar){
        try{
//            cout << "moveStarsToXY::appendCSVDataToXYFiles: csvData.size() = " << csvData.size() << endl;
//            cout << "moveStarsToXY::appendCSVDataToXYFiles: keyWordHammerX = " << keyWordHammerX << endl;
//            cout << "moveStarsToXY::appendCSVDataToXYFiles: csvData.getData(keyWordHammerX) = "
//                    << csvData.getData(keyWordHammerX) << endl;
//            cout << "moveStarsToXY::appendCSVDataToXYFiles: csvData.getData(keyWordHammerY) = "
//                    << csvData.getData(keyWordHammerY) << endl;
//            cout << "moveStarsToXY::appendCSVDataToXYFiles: csvData.getData(keyWordHammerX, "
//                    << iStar << ") = " << csvData.getData(keyWordHammerX, iStar) << endl;
//            cout << "moveStarsToXY::appendCSVDataToXYFiles: csvData.getData(keyWordHammerY, "
//                    << iStar << ") = " << csvData.getData(keyWordHammerY, iStar) << endl;
            XY xy(stod(csvData.getData(keyWordHammerX, iStar)),
                  stod(csvData.getData(keyWordHammerY, iStar)));
            bool pixFound = false;
            for (int iPix=0; iPix<pixels.size(); ++iPix){
                if (pixels[iPix].isInside(xy)){
                    // Check if star is already in outFiles[iPix]
                    if (lastEntryFound && doFind){
                        time_t findStart, findEnd;
                        time (&findStart); // note time before execution

                        string lockName = "/var/lock/lock_" + to_string(iPix) + lockSuffix;
                        if (outFiles[iPix]->is_open())
                            closeFilesAndDeleteLocks(filesOpened,
                                                     locks,
                                                     lockFds);
                        int lockFd = lockFile(outFileNames[iPix], lockName);
                        if (lockFd >= 0){
                            CSVData csvDataOutFile = readCSVFile(outFileNames[iPix]);
                            closeFileAndDeleteLock(*(outFiles[iPix]),
                                                   lockName,
                                                   lockFd);
                            int iId = -1;
                            if (ids.size() > 0){
                                for (auto itId=ids.begin(); itId!=ids.end(); ++itId){
                                    ++iId;
                                    cout << "iStar = " << iStar << ": csvDataOutFile.size() = " << csvDataOutFile.size() << ", reading id <" << *itId << ">" << endl;
                                    vector<string> idsTemp = csvDataOutFile.getData(*itId);
                                    cout << "iStar = " << iStar << ": idsTemp.size() = " << idsTemp.size() << endl;
                                    string id = csvData.getData(*itId, iStar);
                                    cout << "iStar = " << iStar << ": checking for " << *itId << " = " << id << " in file " << outFileNames[iPix] << endl;
                                    if (std::find(idsTemp.begin(), idsTemp.end(), id) != idsTemp.end()){
                                        starFoundInIds[iId] = true;
                                        cout << "iStar = " << iStar << ": id <" << id << "> found in " << outFileNames[iPix] << endl;
                                    }
                                    else{
                                        starFoundInIds[iId] = false;
                                        cout << "iStar = " << iStar << ": id <" << id << "> NOT found in " << outFileNames[iPix] << endl;
                                        break;
                                    }
                                }
                                alreadyThere = starFoundInIds[0];
                                for (int iIId = 1; iIId<=iId; ++iIId){
                                    alreadyThere = alreadyThere && starFoundInIds[iIId];
                                }
                                if (!alreadyThere){
                                    lastEntryFound = false;
                                    cout << "iStar = " << iStar << ": star not found in " << outFileNames[iPix] << " => stopping search" << endl;
                                }
                                else{
                                    cout << "iStar = " << iStar << ": alreadyThere == true" << endl;
                                    lastEntryFound = true;
                                }
                            }
                            else{
                                alreadyThere = false;
                                lastEntryFound = false;
                            }
                        }
                        time (&findEnd); // note time after execution
                        cout << "iStar = " << iStar << ": time taken to search for star: " << findEnd-findStart << " s" << endl;
                    }
                    if (!alreadyThere){
                        if (doFind){
                            time (&findsEnd);
                            cout << "time taken to search for stars: " << findsEnd-findsStart << " s" << endl;
                        }
                        if (!outFiles[iPix]->is_open()){
                            openAndLockFile(outFiles,
                                            outFileNames,
                                            filesOpened,
                                            locks,
                                            lockFds,
                                            iPix,
                                            lockSuffix);
                        }
                        if (doWrite){
                            writeStrVecToFile(csvData.data[iStar], *(outFiles[iPix]));
                            ++nStarsWritten;
                        }
                        else
                            cout << "would write csvData.data[" << iStar << "] to <"
                                    << outFileNames[iPix] << "> but not going to as doWrite is false" << endl;
                    }
                    pixFound = true;
                }
            }
            if (!pixFound){
                cout << "ERROR: no pixel found for x = " << xy.x << ", y = " << xy.y << endl;
                exit(EXIT_FAILURE);
            }
        }
        catch (const std::exception& e) { // reference to the base of a polymorphic object
            std::cout << e.what(); // information from length_error printed
            throw;
        }
    }
    cout << "wrote " << nStarsWritten << " stars" << endl;
    cout << "opened " << filesOpened.size() << " files, closing them now" << endl;
    closeFilesAndDeleteLocks(filesOpened,
                             locks,
                             lockFds);
    time (&end); // note time after execution

    cout << "time taken for appendCSVDataToXYFiles(): " << end-start << " s" << endl;

}

void moveStarsToXY(string const& whichOne){
    bool append = false;
    string startWithFileName = "";///Only this file will be checked for already existing entries!

    string dataDirOut;
    vector<string> inputFileNames;
    vector<string> ids(0);

    boost::format fileNameOutRoot;
    if (whichOne.compare("galaxia") == 0){
        dataDirOut = modelGetDataDirOut();
        inputFileNames = galaxiaGetInputFileNames();
        fileNameOutRoot = modelGetFileNameOutRoot();
        ids.push_back("rad");
        ids.push_back("hammerX");
        ids.push_back("hammerY");
        ids.push_back("exbv_solar");
    }
    else if (whichOne.compare("gaia") == 0){
        dataDirOut = gaiaGetDataDirOut();
        inputFileNames = gaiaGetInputFileNames();
        fileNameOutRoot = gaiaGetFileNameOutRoot();
        ids.push_back("source_id");
    }
    else if (whichOne.compare("gaiaTgas") == 0){
        dataDirOut = gaiaTgasGetDataDirOut();
        inputFileNames = gaiaTgasGetInputFileNames();
        fileNameOutRoot = gaiaTgasGetFileNameOutRoot();
        ids.push_back("source_id");
    }
    else if (whichOne.compare("gaiaFromLonLat") == 0){
        dataDirOut = gaiaGetDataDirOut();
        inputFileNames = gaiaGetInputFileNamesFromLonLat();
        fileNameOutRoot = gaiaGetFileNameOutRoot();
        ids.push_back("source_id");
    }
    else{
        cout << "moveStarsToXY: ERROR: whichOne(=<" << whichOne << ">) is neither equal to <galaxia> nor to <gaia>" << endl;
        exit(EXIT_FAILURE);
    }
//    cout << "running calcOuterLimits" << endl;
    Hammer hammer;
    hammer.calcOuterLimits();

//    cout << "running getPixels" << endl;
    vector<Pixel> pixels=hammer.getPixels();

    /// open all outFiles and write header
    vector<string> header = readHeader(inputFileNames[0]);
    header.push_back(hammer.getKeyWordHammerX());
    header.push_back(hammer.getKeyWordHammerY());

    writeHeaderToOutFiles(header, pixels, whichOne, append);

//    cout << "reading input files" << endl;
    bool runFile = false;
    for (auto itInputFileName=inputFileNames.begin(); itInputFileName!=inputFileNames.end(); ++itInputFileName){
        if (!runFile &&
                (!append ||
                 (append && (itInputFileName->compare(startWithFileName) == 0))
                )
           ){
            runFile = true;
        }
        if (runFile){
//            cout << "reading fileName <" << *itInputFileName << ">" << endl;
            CSVData csvData = readCSVFile(*itInputFileName);
            vector<string> lonStr = csvData.getData(string("l"));
            vector<string> latStr = csvData.getData(string("b"));
            vector<double> lonDbl = convertStringVectorToDoubleVector(lonStr);
            vector<double> latDbl = convertStringVectorToDoubleVector(latStr);
            for (int iLine=0; iLine<lonDbl.size(); ++iLine){
                LonLat lonLat;
                lonLat.lon=lonDbl[iLine];
                lonLat.lat=latDbl[iLine];
                XY xy = hammer.lonLatToXY(lonLat);
                csvData.data[iLine].push_back(to_string(xy.x));
                csvData.data[iLine].push_back(to_string(xy.y));
            }
            appendCSVDataToXYFiles(csvData, pixels, whichOne, ids);
        }
        else{
            cout << "skipping file " << *itInputFileName << endl;
        }
    }
    return;
}

vector<string> galaxiaGetLonLatFileNames(){
    string dataDir("/Volumes/yoda/azuri/data/galaxia/");
    boost::format fileNameRoot = boost::format("galaxia_%i-%i_%i-%i.csv");// % (int(minLongitude), int(maxLongitude), int(minLatitude), int(maxLatitude))

    vector<string> out(0);
    out.reserve(36*18);
    for (int iLon=-180; iLon<180; iLon+=10){
        for (int iLat=-90; iLat<90; iLat+=10){
            out.push_back(dataDir + (fileNameRoot % iLon
                                                  % (iLon+10)
                                                  % iLat
                                                  % (iLat+10)).str());
            if (!ifstream(out[out.size()-1])){
                cout << "galaxiaGetLonLatFileNames: ERROR: file <" << out[out.size()-1] << "> does not exist" << endl;
                exit(EXIT_FAILURE);
            }
        }
    }
    return out;
}

void galaxiaFixHeaderLineEnd(){
    vector<string> lonLatFileNames = galaxiaGetLonLatFileNames();
    for (auto itFileName=lonLatFileNames.begin(); itFileName!=lonLatFileNames.begin()+1; ++itFileName){//lonLatFileNames.end(); ++itFileName){
        cout << "reading <" << *itFileName << ">" << endl;
        CSVData csvData = readCSVFile(*itFileName);
        cout << "csvData.header.size() = " << csvData.header.size() << ", csvData.data.size() = "
                << csvData.data.size() << ", csvData.data[0].size() = " << csvData.data[0].size() << endl;
        if (csvData.header.size() != csvData.data[0].size()){
            cout << "header size and data size differ, gonna fix that..." << endl;
        }
    }
    return;
}

void checkGaiaInputFiles(){
    std::string dataDir("/Volumes/external/azuri/data/gaia/cdn.gea.esac.esa.int/Gaia/gaia_source/csv/");
    boost::format fileNameRoot = boost::format("GaiaSource_%03i-%03i-%03i.csv");//% (release, tract, patch)

    float lon, lat;
    for (int iRelease=0; iRelease<3; ++iRelease){
        for (int iTract=0; iTract<1000; ++iTract){
            for (int iPatch=0; iPatch<1000; ++iPatch){
                std::string fileName = dataDir + (fileNameRoot % iRelease % iTract % iPatch).str();
                if (ifstream(fileName)){/// File exists
                    std::cout << "reading fileName <" << fileName << ">" << std::endl;
                    CSVData csvData = readCSVFile(fileName);
                }
            }
        }
    }
}

//int main(){
////    galaxiaMoveStarsFromEBFToXY();
//    gaiaTgasMoveStarsToXY();
//    return 0;
//}

