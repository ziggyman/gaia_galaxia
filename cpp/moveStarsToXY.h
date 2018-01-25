#ifndef __MOVESTARSTOXY__
#define __MOVESTARSTOXY__

#include <algorithm>
#include <boost/format.hpp>
#include <cstdio>
#include <ctime> // time_t
#include <fcntl.h>
#include <sys/file.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <vector>

#include "csvData.h"
#include "filesAndLocks.h"
#include "hammer.h"
#include "parameters.h"

using namespace std;

vector<string> galaxiaGetInputFileNames();
vector<string> gaiaGetInputFileNames();
vector<string> gaiaTgasGetInputFileNames();
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
                            string const& whichOne,
                            vector<string> const& ids,
                            bool const& doFind=false);
//                            vector< std::shared_ptr< ofstream > > const& outFiles,
//                            vector<string> const& outFileNames);

void gaiaMoveStarsToXY();

void gaiaTgasMoveStarsToXY();

void gaiaMoveStarsFromLonLatToXY();

void galaxiaMoveStarsFromLonLatToXY();

void moveStarsToXY(string const& whichOne);

vector<string> galaxiaGetLonLatFileNames();

void galaxiaFixHeaderLineEnd();

/**
 * @brief Check Gaia Input Files for the same number of elements per line
 */
void checkGaiaInputFiles();

//int main();

#endif
