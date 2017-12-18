#include "moveStarsToXY.h"

void gaiaMoveStarsToXY(){
    bool append = true;
    bool doWrite = false;
    double startWithLon = 170.0;
    double startWithLat = -80.0;

    string dataDir("/Volumes/external/azuri/data/gaia/lon-lat/");
    boost::format fileNameRoot = boost::format("GaiaSource_%i-%i_%i-%i.csv");// % (int(minLongitude), int(maxLongitude), int(minLatitude), int(maxLatitude))

    string dataDirOut("/Volumes/external/azuri/data/gaia/xy/");
    boost::format fileNameOutRoot = boost::format("GaiaSource_%06f-%06f_%06f-%06f.csv");// % (float(minX), float(maxX), float(minY), float(maxY))

    cout << "running calcOuterLimits" << endl;
    Hammer hammer;
    hammer.calcOuterLimits();

    cout << "running getPixels" << endl;
    vector<Pixel> pixels=hammer.getPixels();

    cout << "creating vectors for longitudes and latitudes" << endl;
    vector<int> longitudes(0);
    vector<int> latitudes(0);
    for (int lon=0; lon<=360; lon+=10)
        longitudes.push_back(lon);
    for (int lat=-90; lat<=90; lat+=10)
        latitudes.push_back(lat);

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
    string fileName = dataDir + (fileNameRoot % longitudes[longitudes.size()-2]
                                              % longitudes[longitudes.size()-1]
                                              % latitudes[latitudes.size()-2]
                                              % latitudes[latitudes.size()-1]).str();
    cout << "running readHeader for " << fileName << endl;
    vector<string> header = readHeader(fileName);
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

    cout << "reading input lon lat files" << endl;
    vector< std::shared_ptr< ofstream > > filesOpened(0);
    filesOpened.reserve(1000);
    for (int iLon=1; iLon<longitudes.size(); ++iLon){
        for (int iLat=1; iLat<latitudes.size(); ++iLat){
            if (!append ||
                    (append && (((fabs(longitudes[iLon-1] - startWithLon) < 0.000001) && (latitudes[iLat-1] >= startWithLat))
                                || (longitudes[iLon-1] > startWithLon)))){
                XY xyLowLeft = hammer.lonLatToXY(longitudes[iLon-1], latitudes[iLat-1]);
                XY xyLowRight = hammer.lonLatToXY(longitudes[iLon], latitudes[iLat-1]);
                XY xyHighLeft = hammer.lonLatToXY(longitudes[iLon-1], latitudes[iLat]);
                XY xyHighRight = hammer.lonLatToXY(longitudes[iLon], latitudes[iLat]);
                cout << "calculating lonLowLeft = " << longitudes[iLon-1] << ", latLowLeft = "
                     << latitudes[iLat-1] << ": xLowLeft = " << xyLowLeft.x << ", yLowLeft = " << xyLowLeft.y << endl;
                cout << "calculating lonLowRight = " << longitudes[iLon] << ", latLowRight = "
                     << latitudes[iLat-1] << ": xLowRight = " << xyLowRight.x << ", yLowRight = " << xyLowRight.y << endl;
                cout << "calculating lonHighLeft = " << longitudes[iLon-1] << ", latHighLeft = "
                     << latitudes[iLat] << ": xHighLeft = " << xyHighLeft.x << ", yHighLeft = " << xyHighLeft.y << endl;
                cout << "calculating lonHighRight = " << longitudes[iLon] << ", latHighRight = "
                     << latitudes[iLat] << ": xHighRight = " << xyHighRight.x << ", yHighRight = " << xyHighRight.y << endl;
                string fileNameIn = dataDir + (fileNameRoot % longitudes[iLon-1]
                                                          % longitudes[iLon]
                                                          % latitudes[iLat-1]
                                                          % latitudes[iLat]).str();
                cout << "reading fileName <" << fileNameIn << ">" << endl;
                CSVData csvData = readCSVFile(fileNameIn);
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
                    if ((xy.x < (xyLowLeft.x < xyHighLeft.x ? xyLowLeft.x : xyHighLeft.x)) ||
                        (xy.x > (xyHighRight.x > xyLowRight.x ? xyHighRight.x : xyLowRight.x)) ||
                        (xy.y < (xyLowLeft.y < xyLowRight.y ? xyLowLeft.y : xyLowRight.y)) ||
                        (xy.y > (xyHighRight.y > xyHighLeft.y ? xyHighRight.y : xyHighLeft.y)))
                    {
                        string outStr = (boost::format("ERROR: lon[%i] = %12f, lat[%i] = %12f: x=%12f, y=%12f outside [LowLeft, HighRight]")
                                % iLine
                                % lonLat.lon
                                % iLine
                                % lonLat.lat
                                % xy.x
                                % xy.y).str();
                        cout << outStr << endl;
                        cout << "source_id[iLine-1=" << iLine-1 << "] = " << csvData.getData("source_id", iLine-1) << endl;
                        cout << "source_id[iLine=" << iLine << "] = " << csvData.getData("source_id", iLine) << endl;
                        cout << "source_id[iLine+1=" << iLine+1 << "] = " << csvData.getData("source_id", iLine+1) << endl;
                        exit(EXIT_FAILURE);
                    }
                    csvData.data[iLine].push_back(to_string(xy.x));
                    csvData.data[iLine].push_back(to_string(xy.y));
//                    cout << "lon = " << lonDbl[iLine] << ", lat = " << latDbl[iLine] << ": x = " << xy.x << ", y = " << xy.y << endl;
                    bool pixFound = false;
                    for (int iPix=0; iPix<pixels.size(); ++iPix){
                        if (pixels[iPix].isInside(xy)){
                            bool alreadyThere = false;
                            // if lon==startWithLon && lat==startWithLat: Check if star is already in outFiles[iPix]
                            if (append && lastEntryFound &&
                                    ((fabs(longitudes[iLon-1] - startWithLon) < 0.000001) && (fabs(latitudes[iLat-1] - startWithLat) < 0.000001))){
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
                cout << "opened " << filesOpened.size() << " files, closing them now" << endl;
                for (auto open=filesOpened.begin(); open!=filesOpened.end(); ++open)
                    (*open)->close();
                filesOpened.resize(0);
                cout << filesOpened.size() << " files still open" << endl;
            }
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
//    gaiaMoveStarsToXY();
    checkGaiaInputFiles();
    return 0;
}

