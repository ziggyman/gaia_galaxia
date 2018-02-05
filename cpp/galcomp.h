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
#include "galaxyMath.h"
#include "parameters.h"

using namespace std;

int existsHowManyTimes(vector<string> const& inVec, string const& in);

void countStars(vector<Pixel> const& pixels, int const& pixelId, string const& outFileName, string const& whichOne="gaia");

vector< vector< string > > getGaiaObject(CSVData const& csvData, string const& source_id);

string getCSVFileName(Pixel const& pixel, string const& whichOne);

vector<string> getHeader(string const& whichOne);

vector<Pixel> getPixelsInXYWindow(vector<Pixel> const& pixelsIn, Pixel const& windowIn);

CSVData getStarsInXYWindow(vector<Pixel> const& pixelsIn, Pixel const& window, string const& whichOne);

void simulateObservation(vector<Pixel> const& pixels,
                         Pixel const& xyWindow,
                         string const& filter,
                         string const& whichGaia);

void comparePixel(vector<Pixel> const& pixels, 
                  Pixel const& xyWindow,
                  string const& keyWord,
                  string const& whichObs);

vector<double> getGaiaG(CSVData const& csvData);

#endif
