#include <boost/format.hpp>
#include <vector>
#include "hammer.h"
#include "galcomp.h"

using namespace std;

void gaiaMoveStarsToXY{
    string dataDir("/Volumes/external/azuri/data/gaia/lon-lat/");
    boost::format fileNameRoot = boost::format("GaiaSource_%i-%i_%i-%i.csv");// % (int(minLongitude), int(maxLongitude), int(minLatitude), int(maxLatitude))

    string dataDirOut("/Volumes/external/azuri/data/gaia/xy");
    boost::format fileNameOutRoot = boost::format("GaiaSource_%06fn-%06fn_%06fn-%06fn.csv");// % (float(minX), float(maxX), float(minY), float(maxY))

    calcOuterLimits();
    vector<Pixel> pixels=getPixels();

    vector<ofstream> outFiles(0);
    outFiles.reserve(pixels.size);

    vector<int> longitudes(0);
    vector<int> latitudes(0);
    for (int lon=5; lon<360; lon+=10)
        longitudes.push_back(lon);
    for (int lat=-85; lat<90; lat+=10)
        latitudes.push_back(lat);

    string fileName = dataDir + (fileNameRoot % longitudes[0]
                                              % longitudes[1]
                                              % latitudes[0]
                                              % latitudes[1]).str();
    vector<string> header = readHeader(fileName);
    header.push_back("hammerX");
    header.push_back("hammerY");
    for (int iPix=0; iPix<pixels.size(); ++iPix){
        string outFileName = dataDirOut + (fileNameOutRoot % pixels[iPix].xLow
                                                           % pixels[iPix].xHigh
                                                           % pixels[iPix].yLow
                                                           % pixels[iPix].yHigh);
        ofstream outFile;
        outFile.open(outFileName);
        writeStrVecToFile(header, outFile);
        outFiles.push_back(outFile);
    }

    for (int iLon=1; iLon<longitudes.size(); ++iLon){
        for (int iLat=1; iLst<latitudes.size(); ++iLat){
            string fileName = dataDir + (fileNameRoot % longitudes[iLon-1]
                                                      % longitudes[iLon]
                                                      % latitudes[iLat-1]
                                                      % latitudes[iLat]).str();
            cout << "reading fileName <" << fileName << ">" << endl;
            CSVData csvData = readCSVFile(fileName);
            vector<string> lonStr = csvData.getData(string("l"));
            vector<string> latStr = csvData.getData(string("b"));
            vector<double> lonDbl = convertStringVectortoDoubleVector(lonStr);
            vector<double> latDbl = convertStringVectortoDoubleVector(latStr);
            for (int iLine=0; iLine<lonDbl.size(); ++iLine){
                LonLat lonLat;
                lonLat.lon=lonDbl[iLine];
                lonLat.lat=latDbl[iLine];
                XY xy = lonLatToXY(lonLat);
                csvData.data.push_back(to_string(xy.x));
                csvData.data.push_back(to_string(xy.yu));
                cout << 'lon = ' << lonLat.lon << ", lat = " << lonLat.lat << ": x = " << xy.x << ", y = " << xy.y << endl;
                bool pixFound = false;
                for (int iPix=0; iPix<pixels.size(); ++iPix){
                    if (isInPixel(pixels[iPix], xy)){
                        writeStrVecToFile(csvData.data, outFiles[iPix]);
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

    for (int iPix=0; iPix<pixels.size(); ++iPix){
        outFiles[iPix].close();
    }
    return;
}
