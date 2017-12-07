#include <boost/format.hpp>
#include <vector>
#include "hammer.h"
#include "galcomp.h"

using namespace std;

void gaiaMoveStarsToXY(){
    string dataDir("/Volumes/external/azuri/data/gaia/lon-lat/");
    boost::format fileNameRoot = boost::format("GaiaSource_%i-%i_%i-%i.csv");// % (int(minLongitude), int(maxLongitude), int(minLatitude), int(maxLatitude))

    string dataDirOut("/Volumes/external/azuri/data/gaia/xy/");
    boost::format fileNameOutRoot = boost::format("GaiaSource_%06f-%06f_%06f-%06f.csv");// % (float(minX), float(maxX), float(minY), float(maxY))

    cout << "running calcOuterLimits" << endl;
    calcOuterLimits();

    cout << "running getPixels" << endl;
    vector<Pixel> pixels=getPixels();

    cout << "creating vector of outFiles" << endl;
    vector< std::shared_ptr< ofstream > > outFiles(0);
    outFiles.reserve(pixels.size());

    cout << "creating vectors for longitudes and latitudes" << endl;
    vector<int> longitudes(0);
    vector<int> latitudes(0);
    for (int lon=0; lon<=360; lon+=10)
        longitudes.push_back(lon);
    for (int lat=-90; lat<=90; lat+=10)
        latitudes.push_back(lat);

    string fileName = dataDir + (fileNameRoot % longitudes[longitudes.size()-2]
                                              % longitudes[longitudes.size()-1]
                                              % latitudes[latitudes.size()-2]
                                              % latitudes[latitudes.size()-1]).str();
    cout << "running readHeader for " << fileName << endl;
    vector<string> header = readHeader(fileName);
    header.push_back("hammerX");
    header.push_back("hammerY");
    
    cout << "opening outfiles and writing headers" << endl;
    int nOpenFiles = 0;
    for (int iPix=0; iPix<pixels.size(); ++iPix){
        string outFileName = dataDirOut + (fileNameOutRoot % pixels[iPix].xLow
                                                           % pixels[iPix].xHigh
                                                           % pixels[iPix].yLow
                                                           % pixels[iPix].yHigh).str();
        std::shared_ptr<ofstream> outFile(new ofstream);
        outFile->exceptions(ofstream::failbit | ofstream::badbit);
        outFile->open(outFileName);
        if (!outFile->is_open()){
            cout << "gaiaMoveStarsToXY: ERROR: Failed to open outFile = <"
                 << outFileName << ">, nOpenFiles = " << nOpenFiles << endl;
            exit(EXIT_FAILURE);
        }
        writeStrVecToFile(header, *outFile);
        outFiles.push_back(outFile);
        ++nOpenFiles;
    }

    cout << "reading input lon lat files" << endl;
    for (int iLon=1; iLon<longitudes.size(); ++iLon){
        for (int iLat=1; iLat<latitudes.size(); ++iLat){
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
            for (int iLine=0; iLine<lonDbl.size(); ++iLine){
                LonLat lonLat;
                lonLat.lon=lonDbl[iLine];
                lonLat.lat=latDbl[iLine];
                XY xy = lonLatToXY(lonLat);
                csvData.data[iLine].push_back(to_string(xy.x));
                csvData.data[iLine].push_back(to_string(xy.y));
                cout << "lon = " << lonLat.lon << ", lat = " << lonLat.lat << ": x = " << xy.x << ", y = " << xy.y << endl;
                bool pixFound = false;
                for (int iPix=0; iPix<pixels.size(); ++iPix){
                    if (isInPixel(pixels[iPix], xy)){
                        writeStrVecToFile(csvData.data[iLine], *(outFiles[iPix]));
                        pixFound = true;
                    }
                }
                if (!pixFound){
                    cout << "ERROR: no pixel found for lon = " << lonLat.lon << ", lat = " << lonLat.lat << endl;
                    exit(EXIT_FAILURE);
                }
            }
        }
    }

    cout << "closing outfiles" << endl;
    for (int iPix=0; iPix<pixels.size(); ++iPix){
        outFiles[iPix]->close();
    }
    return;
}
