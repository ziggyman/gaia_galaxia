#ifndef __MOVESTARSTOXY__
#define __MOVESTARSTOXY__

#include <algorithm>
#include <boost/format.hpp>
#include <vector>
#include "galcomp.h"

using namespace std;

boost::format galaxiaGetFileNameOutRoot();
boost::format gaiaGetFileNameOutRoot();

string galaxiaGetDataDirOut();
string gaiaGetDataDirOut();

vector<string> galaxiaGetInputFileNames();
vector<string> gaiaGetInputFileNames();
vector<string> gaiaGetInputFileNamesFromLonLat();

vector< std::shared_ptr< ofstream > > getOutFiles(vector<Pixel> const& pixels);

vector<string> getOutFileNames(vector<Pixel> const& pixels,
                               string const& whichOne);

void writeHeaderToOutFiles(vector<string> const& header,
                           vector<Pixel> const& pixels,
                           string const& whichOne,
                           bool const& append);
//                           vector<string> const& outFileNames,
//                           vector< std::shared_ptr< ofstream > > const& outFiles);

void appendCSVDataToXYFiles(CSVData const& csvData,
                            vector<Pixel> const& pixels,
                            string const& whichOne);
//                            vector< std::shared_ptr< ofstream > > const& outFiles,
//                            vector<string> const& outFileNames);

void gaiaMoveStarsToXY();

void gaiaMoveStarsFromLonLatToXY();

void galaxiaMoveStarsFromLonLatToXY();

void moveStarsToXY(string const& whichOne);

vector<string> galaxiaGetLonLatFileNames();

void galaxiaFixHeaderLineEnd();

/**
 * @brief Check Gaia Input Files for the same number of elements per line
 */
void checkGaiaInputFiles();

int main();

#endif
