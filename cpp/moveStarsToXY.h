#include <boost/format.hpp>
#include <vector>
#include "hammer.h"
#include "galcomp.h"

using namespace std;

void gaiaMoveStarsToXY(){
    bool append = false;
    double startWithLon = 90.0;
    double startWithLat = -90.0;

    string dataDir("/Volumes/external/azuri/data/gaia/lon-lat/");
    boost::format fileNameRoot = boost::format("GaiaSource_%i-%i_%i-%i.csv");// % (int(minLongitude), int(maxLongitude), int(minLatitude), int(maxLatitude))

    string dataDirOut("/Volumes/external/azuri/data/gaia/xy/");
    boost::format fileNameOutRoot = boost::format("GaiaSource_%06f-%06f_%06f-%06f.csv");// % (float(minX), float(maxX), float(minY), float(maxY))

    cout << "running calcOuterLimits" << endl;
    calcOuterLimits();

    cout << "running getPixels" << endl;
    vector<Pixel> pixels=getPixels();

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
                XY xyLowLeft = lonLatToXY(longitudes[iLon-1], latitudes[iLat-1]);
                XY xyLowRight = lonLatToXY(longitudes[iLon], latitudes[iLat-1]);
                XY xyHighLeft = lonLatToXY(longitudes[iLon-1], latitudes[iLat]);
                XY xyHighRight = lonLatToXY(longitudes[iLon], latitudes[iLat]);
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
                for (int iLine=0; iLine<lonDbl.size(); ++iLine){
                    LonLat lonLat;
                    lonLat.lon=lonDbl[iLine];
                    lonLat.lat=latDbl[iLine];
                    XY xy = lonLatToXY(lonLat);
                    if ((xy.x < (xyLowLeft.x < xyHighLeft.x ? xyLowLeft.x : xyHighLeft.x)) ||
                        (xy.x > (xyHighRight.x > xyLowRight.x ? xyHighRight.x : xyLowRight.x)) ||
                        (xy.y < (xyLowLeft.y < xyLowRight.y ? xyLowLeft.y : xyLowRight.y)) ||
                        (xy.y > (xyHighRight.y > xyHighLeft.y ? xyHighRight.y : xyHighLeft.y))){
                        cout << "ERROR: x=" << xy.x << ", y=" << xy.y << " outside [LowLeft, HighRight]" << endl;
                        exit(EXIT_FAILURE);
                    }
                    csvData.data[iLine].push_back(to_string(xy.x));
                    csvData.data[iLine].push_back(to_string(xy.y));
    //                cout << "lon = " << lonLat.lon << ", lat = " << lonLat.lat << ": x = " << xy.x << ", y = " << xy.y << endl;
                    bool pixFound = false;
                    for (int iPix=0; iPix<pixels.size(); ++iPix){
                        if (isInPixel(pixels[iPix], xy)){
                            if (!outFiles[iPix]->is_open()){
                                outFiles[iPix]->open(outFileNames[iPix], ofstream::app);
                                filesOpened.push_back(outFiles[iPix]);
                                cout << "opened file <" << outFileNames[iPix] << ">" << endl;
                            }
                            writeStrVecToFile(csvData.data[iLine], *(outFiles[iPix]));
                            pixFound = true;
                        }
                    }
                    if (!pixFound){
                        cout << "ERROR: no pixel found for lon = " << lonLat.lon << ", lat = " << lonLat.lat << endl;
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
