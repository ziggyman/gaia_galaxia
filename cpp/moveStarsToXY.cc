#include "moveStarsToXY.h"

boost::format galaxiaGetFileNameOutRoot(){
    return boost::format("galaxia_%06f-%06f_%06f-%06f.csv");// % (float(minX), float(maxX), float(minY), float(maxY))
}

boost::format gaiaGetFileNameOutRoot(){
    return boost::format("GaiaSource_%06f-%06f_%06f-%06f.csv");// % (float(minX), float(maxX), float(minY), float(maxY))
}

string galaxiaGetDataDirOut(){
    return "/Volumes/yoda/azuri/data/galaxia/xy/";
}

string gaiaGetDataDirOut(){
    return "/Volumes/external/azuri/data/gaia/xy/";
}

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
        fileNameOutRoot = galaxiaGetFileNameOutRoot();
        dataDirOut = galaxiaGetDataDirOut();
    }
    else if (whichOne.compare("gaia") == 0){
        fileNameOutRoot = gaiaGetFileNameOutRoot();
        dataDirOut = gaiaGetDataDirOut();
    }
    else{
        cout << "getOutFileNames: ERROR: whichOne(=<" << whichOne << ">) neither equal to <galaxia> nor to <gaia>" << endl;
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

void gaiaMoveStarsFromLonLatToXY(){
    moveStarsToXY("gaiaFromLonLat");
}

void galaxiaMoveStarsFromLonLatToXY(){
    moveStarsToXY("galaxia");
}

void appendCSVDataToXYFiles(CSVData const& csvData,
                            vector<Pixel> const& pixels,
                            string const& whichOne){
    bool doWrite = true;
    Hammer ham;

    vector< std::shared_ptr< ofstream > > const& outFiles = getOutFiles(pixels);
    vector<string> const& outFileNames = getOutFileNames(pixels, whichOne);

    vector< std::shared_ptr< ofstream > > filesOpened(0);
    filesOpened.reserve(1000);

    int nStarsWritten = 0;
    for (int iStar=0; iStar<csvData.size(); ++iStar){
        XY xy(stod(csvData.getData(ham.getKeyWordHammerX(), iStar)),
              stod(csvData.getData(ham.getKeyWordHammerY(), iStar)));
        bool pixFound = false;
        for (int iPix=0; iPix<pixels.size(); ++iPix){
            if (pixels[iPix].isInside(xy)){
                // if lon==startWithLon && lat==startWithLat: Check if star is already in outFiles[iPix]
/*                if (append && lastEntryFound &&
                        (itInputFileName->compare(startWithFileName) == 0)){
                    CSVData csvDataOutFile = readCSVFile(outFileNames[iPix]);
                    cout << "csvDataOutFile.size() = " << csvDataOutFile.size() << ", reading source_ids" << endl;
                    vector<string> ids = csvDataOutFile.getData("source_id");
                    cout << "ids.size() = " << ids.size() << endl;
                    string source_id = csvData.getData("source_id", iStar);
                    cout << "checking for source_id = " << source_id << " in source_ids" << endl;
                    if (std::find(ids.begin(), ids.end(), source_id) != ids.end()){
                        alreadyThere = true;
                        cout << "source_id <" << source_id << "> found in " << outFileNames[iPix] << endl;
                    }
                    else{
                        lastEntryFound = false;
                        cout << "source_id <" << source_id << "> not found in " << outFileNames[iPix] << " => stopping search" << endl;
                    }
                }*/
                if (!outFiles[iPix]->is_open()){
                    outFiles[iPix]->open(outFileNames[iPix], ofstream::app);
                    filesOpened.push_back(outFiles[iPix]);
                    cout << "opened file <" << outFileNames[iPix] << ">" << endl;
                }
//                if (!alreadyThere){
                if (doWrite){
                    writeStrVecToFile(csvData.data[iStar], *(outFiles[iPix]));
                    ++nStarsWritten;
                }
                else
                    cout << "would write csvData.data[" << iStar << "] to <"
                            << outFileNames[iPix] << "> but not going to as doWrite is false" << endl;
//                }
                pixFound = true;
            }
        }
        if (!pixFound){
            cout << "ERROR: no pixel found for x = " << xy.x << ", y = " << xy.y << endl;
            exit(EXIT_FAILURE);
        }
    }
    cout << "wrote " << nStarsWritten << " stars" << endl;
    cout << "opened " << filesOpened.size() << " files, closing them now" << endl;
    for (auto open=filesOpened.begin(); open!=filesOpened.end(); ++open)
        (*open)->close();
    filesOpened.resize(0);
}

void moveStarsToXY(string const& whichOne){
    bool append = false;
    string startWithFileName = "";///Only this file will be checked for already existing entries!

    string dataDirOut;
    vector<string> inputFileNames;

    boost::format fileNameOutRoot;
    if (whichOne.compare("galaxia") == 0){
        dataDirOut = galaxiaGetDataDirOut();
        inputFileNames = galaxiaGetInputFileNames();
        fileNameOutRoot = galaxiaGetFileNameOutRoot();
    }
    else if (whichOne.compare("gaia") == 0){
        dataDirOut = gaiaGetDataDirOut();
        inputFileNames = gaiaGetInputFileNames();
        fileNameOutRoot = gaiaGetFileNameOutRoot();
    }
    else if (whichOne.compare("gaiaFromLonLat") == 0){
        dataDirOut = gaiaGetDataDirOut();
        inputFileNames = gaiaGetInputFileNamesFromLonLat();
        fileNameOutRoot = gaiaGetFileNameOutRoot();
    }
    else{
        cout << "moveStarsToXY: ERROR: whichOne(=<" << whichOne << ">) is neither equal to <galaxia> nor to <gaia>" << endl;
        exit(EXIT_FAILURE);
    }
    cout << "running calcOuterLimits" << endl;
    Hammer hammer;
    hammer.calcOuterLimits();

    cout << "running getPixels" << endl;
    vector<Pixel> pixels=hammer.getPixels();

    ///create vectors of outFileNames and outFiles
    vector< std::shared_ptr< ofstream > > outFiles = getOutFiles(pixels);
    vector<string> outFileNames = getOutFileNames(pixels, whichOne);

    /// open all outFiles and write header
    vector<string> header = readHeader(inputFileNames[0]);
    header.push_back(hammer.getKeyWordHammerX());
    header.push_back(hammer.getKeyWordHammerY());

    writeHeaderToOutFiles(header, pixels, whichOne, append);

    cout << "reading input files" << endl;
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
            cout << "reading fileName <" << *itInputFileName << ">" << endl;
            CSVData csvData = readCSVFile(*itInputFileName);
            vector<string> lonStr = csvData.getData(string("l"));
            vector<string> latStr = csvData.getData(string("b"));
            vector<double> lonDbl = convertStringVectortoDoubleVector(lonStr);
            vector<double> latDbl = convertStringVectortoDoubleVector(latStr);
            for (int iLine=0; iLine<lonDbl.size(); ++iLine){
                LonLat lonLat;
                lonLat.lon=lonDbl[iLine];
                lonLat.lat=latDbl[iLine];
                XY xy = hammer.lonLatToXY(lonLat);
                csvData.data[iLine].push_back(to_string(xy.x));
                csvData.data[iLine].push_back(to_string(xy.y));
            }
            appendCSVDataToXYFiles(csvData, pixels, whichOne);
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
    struct timeval start, end;
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

int main(){
//    galaxiaMoveStarsFromEBFToXY();
    //gaiaMoveStarsToXY();
    return 0;
}

