#ifndef __GALCOMP_H__
#define __GALCOMP_H__

#include <iostream>
#include <fstream>
#include <string>
#include <sys/time.h>
#include <vector>
#include "csvData.h"
#include "filesAndLocks.h"
#include "hammer.h"
#include "parameters.h"

using namespace std;

int existsHowManyTimes(vector<string> const& inVec, string const& in);

void countStars(vector<Pixel> const& pixels, int const& pixelId, string const& outFileName, string const& whichOne="gaia");

vector< vector< string > > getGaiaObject(CSVData const& csvData, string const& source_id);

CSVData getStarsInXYWindow(Pixel const& window, string const& whichOne);

void comparePixel(Pixel const& pix);

#endif
