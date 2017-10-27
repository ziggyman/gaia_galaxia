#include <boost/format.hpp>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <sys/time.h>

int main(){
    std::string dataDir("/Volumes/external/azuri/data/gaia/cdn.gea.esac.esa.int/Gaia/gaia_source/csv/");
    boost::format fileNameRoot = boost::format("GaiaSource_%03i-%03i-%03i.csv");//% (release, tract, patch)

    std::string outDir("/Volumes/external/azuri/data/gaia/lon-lat/");
    boost::format outFileRoot = boost::format("GaiaSource_%i-%i_%i-%i.csv");// % (int(minLongitude), int(maxLongitude), int(minLatitude), int(maxLatitude))

    std::string filename = dataDir + (fileNameRoot % 0 % 0 % 0).str();
    std::cout << "filename = " << filename << std::endl;

    std::string line, headerLine;
    std::ifstream myfile (filename);
    if (myfile.is_open())
    {
      getline (myfile,headerLine);
      std::cout << headerLine << std::endl;
      myfile.close();
    }
    else std::cout << "Unable to open file" << std::endl;

    std::stringstream ss(headerLine.c_str());
    std::string substring;
    int lPos = -1;
    int bPos = -1;
    int pos = 0;
    while(ss.good()){
        getline(ss, substring, ',');
        if (substring.compare("l") == 0)
            lPos = pos;
        if (substring.compare("b") == 0)
            bPos = pos;
        pos++;
    }
    if (lPos < 0){
        std::cout << "'l' not found" << std::endl;
        exit(EXIT_FAILURE);
    }
    if (bPos < 0){
        std::cout << "'b' not found" << std::endl;
        exit(EXIT_FAILURE);
    }
    std::cout << "lPos = " << lPos << ", bPos = " << bPos << std::endl;

    if (true){
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
        for (int iLon=1; iLon<nLongitudes; ++iLon){
            std::vector< std::shared_ptr< std::ofstream > > files(0);
            for (int iLat=1; iLat<nLatitudes; ++iLat){
                std::string outFileName = outDir + (outFileRoot % longitudes[iLon-1] % longitudes[iLon] % latitudes[iLat-1] % latitudes[iLat]).str();
                std::shared_ptr< std::ofstream > tmpFile(new std::ofstream);
                tmpFile->open(outFileName.c_str());
                if (tmpFile->is_open()){
                    files.push_back(tmpFile);
                    *tmpFile << headerLine << std::endl;
                }
                else{
                    std::cout << "ERROR: Failed to open " << outFileName << std::endl;
                }
            }
            outFiles.push_back(files);
        }

        float lon, lat;
        struct timeval start, end;
        for (int iRelease=0; iRelease<3; ++iRelease){
            for (int iTract=0; iTract<1000; ++iTract){
                for (int iPatch=0; iPatch<1000; ++iPatch){
                    ///start timer
                    gettimeofday(&start, NULL);

                    std::string fileName = dataDir + (fileNameRoot % iRelease % iTract % iPatch).str();
                    std::cout << "reading fileName <" << fileName << ">" << std::endl;
                    std::ifstream inStream(fileName);
                    if (inStream.is_open()){
                        int iLine = 0;
                        std::string line;
                        while (std::getline(inStream, line)){
                            if (iLine == 0){
                                iLine = 1;
                                continue;
                            }
                            std::stringstream lineStream(line.c_str());
                            pos = 0;
                            while(lineStream.good()){
                                getline(lineStream, substring, ',');
                                if (pos == lPos)
                                    lon = stof(substring);
                                if (pos == bPos){
                                    lat = stof(substring);
                                    break;
                                }
                                pos++;
                            }

                            bool found = false;
                            for (int iLon=1; iLon<nLongitudes; ++iLon){
                                for (int iLat=1; iLat<nLatitudes; ++iLat){
                                    if (lon > int(longitudes[iLon-1])
                                        && lon <= int(longitudes[iLon]))
                                    {
                                        if (lat > int(latitudes[iLat-1])
                                            && lat <= int(latitudes[iLat]))
                                        {
                                            *(outFiles[iLon-1][iLat-1]) << line << std::endl;
                                            found = true;
                                        }
                                    }
                                }
                            }
                            if (!found){
                                std::cout << "ERROR: longitude " << lon << ", latitude " << lat << " not found" << std::endl;
                                exit(EXIT_FAILURE);
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
        /// close all output files
        for (int iLon=0; iLon<nLongitudes-1; ++iLon){
            for (int iLat=0; iLat<nLatitudes-1; ++iLat){
                outFiles[iLon][iLat]->close();
            }
        }
    }
}
