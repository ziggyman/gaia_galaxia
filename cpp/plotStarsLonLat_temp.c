#include <boost/format.hpp>
//#include <chrono>
//#include <ctime>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <sys/time.h>

int main(){
    std::string dataDir("/Volumes/external/azuri/data/gaia/lon-lat/");
    boost::format fileNameRoot = boost::format("GaiaSource_%i-%i_%i-%i.csv");// % (int(minLongitude), int(maxLongitude), int(minLatitude), int(maxLatitude))

    std::string filename = dataDir + (fileNameRoot % 0 % 10 % 0 %10).str();
    std::cout << "filename = " << filename << std::endl;

    int lPos = 53;
    int bPos = 54;
    int pos = 0;

    int stepLon = 10;
    int stepLat = 10;

    std::vector<int> longitudes(0);
    std::vector<int> latitudes(0);
    for (int lon=0; lon <= 360; lon+=stepLon){
        longitudes.push_back(lon);
        std::cout << "longitudes[" << longitudes.size()-1 << "] = " << longitudes[longitudes.size()-1] << std::endl;
    }
    for (int lat=-90.0; lat<=90.0; lat+=stepLat){
        latitudes.push_back(lat);
        std::cout << "latitudes[" << latitudes.size()-1 << "] = " << latitudes[latitudes.size()-1] << std::endl;
    }

    int nLongitudes = longitudes.size();
    int nLatitudes = latitudes.size();
    std::cout << "nLongitudes = " << nLongitudes << std::endl;
    std::cout << "nLatitudes = " << nLatitudes << std::endl;

    /// open all output files and put them into a vector
    std::vector< std::vector< std::shared_ptr< std::ofstream > > > outFiles(0);

    float lon, lat;
    struct timeval start, end;
    for (int iLon=1; iLon<nLongitudes; ++iLon){
        for (int iLat=1; iLat<nLatitudes; ++iLat){
            ///start timer

            gettimeofday(&start, NULL);

            std::string fileName = dataDir + (fileNameRoot % longitudes[iLon-1] % longitudes[iLon] % latitudes[iLat-1] % latitudes[iLat]).str();
            std::cout << "reading fileName <" << fileName << ">" << std::endl;
            std::ifstream inStream(fileName);
            if (inStream.is_open()){
                int iLine = 0;
                std::string line;
                while (std::getline(inStream, line)){
//                    if (iLine == 0){
//                        iLine = 1;
//                        continue;
//                    }
                    std::stringstream lineStream(line.c_str());
                    pos = 0;
                    while(lineStream.good()){
                        getline(lineStream, substring, ',');
                        if (pos == lPos)
                            lon = stof(substring);
                        if (pos == bPos){
                            lat = stof(substring);
                            continue;
                        }
                        pos++;
                    }

                }
                inStream.close();
                gettimeofday(&end, NULL);
                std::cout << "fileName <" << fileName << "> read in " << ((end.tv_sec * 1000000 + end.tv_usec)
                                - (start.tv_sec * 1000000 + start.tv_usec))/1000000 << " s" << std::endl;
            }
            else{
                std::cout << "ERROR: Failed to open " << fileName << std::endl;
            }
        }
    }
}
