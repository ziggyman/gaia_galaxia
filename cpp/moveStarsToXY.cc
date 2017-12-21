#include "moveStarsToXY.h"

void gaiaMoveStarsToXY(){
    string dataDir("/Volumes/external/azuri/data/gaia/cdn.gea.esac.esa.int/Gaia/gaia_source/csv/");
    string dataDirOut("/Volumes/external/azuri/data/gaia/xy/");
    boost::format fileNameRoot = boost::format("GaiaSource_%03i-%03i-%03i.csv");//% (release, tract, patch);
    boost::format fileNameOutRoot = boost::format("GaiaSource_%06f-%06f_%06f-%06f.csv");// % (float(minX), float(maxX), float(minY), float(maxY))
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
    moveStarsToXY(dataDir, dataDirOut, inputFileNames, fileNameOutRoot);
}

void gaiaMoveStarsFromLonLatToXY(){
    string dataDir("/Volumes/external/azuri/data/gaia/lon-lat/");
    string dataDirOut("/Volumes/external/azuri/data/gaia/xy/");
    boost::format fileNameRoot = boost::format("GaiaSource_%i-%i_%i-%i.csv");// % (int(minLongitude), int(maxLongitude), int(minLatitude), int(maxLatitude))
    boost::format fileNameOutRoot = boost::format("GaiaSource_%06f-%06f_%06f-%06f.csv");// % (float(minX), float(maxX), float(minY), float(maxY))
    vector<string> inputFileNames(0);
    for (int lon=10; lon<=360; lon+=10){
        for (int lat=-80; lat<=90; lat+=10){
            inputFileNames.push_back(dataDir + (fileNameRoot % (lon-10)
                                                             % lon
                                                             % (lat-10)
                                                             % lat).str());
        }
    }
    moveStarsToXY(dataDir, dataDirOut, inputFileNames, fileNameOutRoot);
}

void galaxiaMoveStarsFromLonLatToXY(){
    string dataDir("/Volumes/yoda/azuri/data/galaxia/lon-lat/");
    string dataDirOut("/Volumes/yoda/azuri/data/galaxia/xy/");
    boost::format fileNameRoot = boost::format("galaxia_%i-%i_%i-%i.csv");// % (int(minLongitude), int(maxLongitude), int(minLatitude), int(maxLatitude))
    boost::format fileNameOutRoot = boost::format("galaxia_%06f-%06f_%06f-%06f.csv");// % (float(minX), float(maxX), float(minY), float(maxY))
    vector<string> inputFileNames(0);
    for (int lon=-80; lon<=180; lon+=10){
        for (int lat=-80; lat<=90; lat+=10){
            inputFileNames.push_back(dataDir + (fileNameRoot % (lon-10)
                                                             % lon
                                                             % (lat-10)
                                                             % lat).str());
        }
    }
    moveStarsToXY(dataDir, dataDirOut, inputFileNames, fileNameOutRoot);
}

void galaxiaMoveStarsFromEBFToXY(){
    string dataDir("/Volumes/yoda/azuri/data/galaxia/lon-lat/");
    string dataDirOut("/Volumes/yoda/azuri/data/galaxia/xy/");
    boost::format fileNameRoot = boost::format("galaxia_%i-%i_%i-%i.csv");// % (int(minLongitude), int(maxLongitude), int(minLatitude), int(maxLatitude))
    boost::format fileNameOutRoot = boost::format("galaxia_%06f-%06f_%06f-%06f.csv");// % (float(minX), float(maxX), float(minY), float(maxY))
    vector<string> inputFileNames(0);
    for (int lon=-80; lon<=180; lon+=10){
        for (int lat=-80; lat<=90; lat+=10){
            inputFileNames.push_back(dataDir + (fileNameRoot % (lon-10)
                                                             % lon
                                                             % (lat-10)
                                                             % lat).str());
        }
    }
    moveStarsToXY(dataDir, dataDirOut, inputFileNames, fileNameOutRoot);
}
void moveStarsToXY(string const& dataDir, string const& dataDirOut, vector<string> const& inputFileNames, boost::format & fileNameOutRoot){
    bool append = false;
    bool doWrite = true;
    string startWithFileName = "";///Only this file will be checked for already existing entries!

    cout << "running calcOuterLimits" << endl;
    Hammer hammer;
    hammer.calcOuterLimits();

    cout << "running getPixels" << endl;
    vector<Pixel> pixels=hammer.getPixels();

    ///create vectors of outFileNames and outFiles
    vector< std::shared_ptr< ofstream > > outFiles(0);
    outFiles.reserve(pixels.size());
    vector<string> outFileNames(0);
    outFileNames.reserve(pixels.size());
    for (int iPix=0; iPix<pixels.size(); ++iPix){
        string outFileName = dataDirOut + (fileNameOutRoot % pixels[iPix].xLow
                                                           % pixels[iPix].xHigh
                                                           % pixels[iPix].yLow
                                                           % pixels[iPix].yHigh).str();
        outFileNames.push_back(outFileName);
        std::shared_ptr<ofstream> outFile(new ofstream);
        outFiles.push_back(outFile);
    }

    /// open all outFiles and write header
    vector<string> header = readHeader(inputFileNames[0]);
    header.push_back("hammerX");
    header.push_back("hammerY");

    cout << "opening outfiles and writing headers" << endl;
    for (int iPix=0; iPix<pixels.size(); ++iPix){
        outFiles[iPix]->exceptions(ofstream::failbit | ofstream::badbit);
        if (!ifstream(outFileNames[iPix]))
            cout << "outFile <" << outFileNames[iPix] << "> does not exist yet" << endl;
        if (!append || !ifstream(outFileNames[iPix])){
            outFiles[iPix]->open(outFileNames[iPix]);
            writeStrVecToFile(header, *outFiles[iPix]);
            outFiles[iPix]->close();
        }
    }

    cout << "reading input files" << endl;
    vector< std::shared_ptr< ofstream > > filesOpened(0);
    filesOpened.reserve(1000);
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
            bool lastEntryFound = true;
            for (int iLine=0; iLine<lonDbl.size(); ++iLine){
                LonLat lonLat;
                lonLat.lon=lonDbl[iLine];
                lonLat.lat=latDbl[iLine];
                XY xy = hammer.lonLatToXY(lonLat);
                csvData.data[iLine].push_back(to_string(xy.x));
                csvData.data[iLine].push_back(to_string(xy.y));

                bool pixFound = false;
                for (int iPix=0; iPix<pixels.size(); ++iPix){
                    if (pixels[iPix].isInside(xy)){
                        bool alreadyThere = false;
                        // if lon==startWithLon && lat==startWithLat: Check if star is already in outFiles[iPix]
                        if (append && lastEntryFound &&
                                (itInputFileName->compare(startWithFileName) == 0)){
                            CSVData csvDataOutFile = readCSVFile(outFileNames[iPix]);
                            cout << "csvDataOutFile.size() = " << csvDataOutFile.size() << ", reading source_ids" << endl;
                            vector<string> ids = csvDataOutFile.getData("source_id");
                            cout << "ids.size() = " << ids.size() << endl;
                            string source_id = csvData.getData("source_id", iLine);
                            cout << "checking for source_id = " << source_id << " in source_ids" << endl;
                            if (std::find(ids.begin(), ids.end(), source_id) != ids.end()){
                                alreadyThere = true;
                                cout << "source_id <" << source_id << "> found in " << outFileNames[iPix] << endl;
                            }
                            else{
                                lastEntryFound = false;
                                cout << "source_id <" << source_id << "> not found in " << outFileNames[iPix] << " => stopping search" << endl;
                            }
                        }
                        if (!outFiles[iPix]->is_open()){
                            outFiles[iPix]->open(outFileNames[iPix], ofstream::app);
                            filesOpened.push_back(outFiles[iPix]);
                            cout << "opened file <" << outFileNames[iPix] << ">" << endl;
                        }
                        if (!alreadyThere){
                            if (doWrite)
                                writeStrVecToFile(csvData.data[iLine], *(outFiles[iPix]));
                            else
                                cout << "would write csvData.data[" << iLine << "] to <"
                                        << outFileNames[iPix] << "> but not going to as doWrite is false" << endl;
                        }
                        pixFound = true;
                    }
                }
                if (!pixFound){
                    cout << "ERROR: no pixel found for lon = " << lonDbl[iLine] << ", lat = " << latDbl[iLine]
                         << ", x = " << xy.x << ", y = " << xy.y << endl;
                    exit(EXIT_FAILURE);
                }
            }
        }
        else{
            cout << "skipping file " << *itInputFileName << endl;
        }
        cout << "opened " << filesOpened.size() << " files, closing them now" << endl;
        for (auto open=filesOpened.begin(); open!=filesOpened.end(); ++open)
            (*open)->close();
        filesOpened.resize(0);
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

