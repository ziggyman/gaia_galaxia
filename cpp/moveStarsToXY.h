#ifndef __MOVESTARSTOXY__
#define __MOVESTARSTOXY__

#include <algorithm>
#include <boost/format.hpp>
#include <vector>
#include "galcomp.h"

using namespace std;

void gaiaMoveStarsToXY();
void gaiaMoveStarsFromLonLatToXY();
void galaxiaMoveStarsFromLonLatToXY();
void moveStarsToXY(string const& dataDir,
                   string const& dataDirOut,
                   vector<string> const& inputFileNames,
                   boost::format & fileNameOutRoot);

vector<string> galaxiaGetLonLatFileNames();

void galaxiaFixHeaderLineEnd();

/**
 * @brief Check Gaia Input Files for the same number of elements per line
 */
void checkGaiaInputFiles();

int main();

#endif
