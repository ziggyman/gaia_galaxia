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

int existsHowManyTimes(vector<string> const& inVec,
                       string const& in);

void countStars(vector<Pixel> const& pixels,
                int const& pixelId,
                string const& outFileName,
                string const& whichOne="gaia");

vector< vector< string > > getGaiaObject(CSVData const& csvData,
                                         string const& source_id);

string getCSVFileName(Pixel const& pixel,
                      string const& whichOne);

vector<string> getHeader(string const& whichOne);

vector<Pixel> getPixelsInXYWindow(vector<Pixel> const& pixelsIn,
                                  Pixel const& windowIn);

CSVData getStarsInXYWindow(vector<Pixel> const& pixelsIn,
                           Pixel const& window,
                           string const& whichOne);

void simulateObservation(vector<Pixel> const& pixels,
                         Pixel const& xyWindow,
                         string const& filter,
                         string const& whichGaia);

void comparePixel(vector<Pixel> const& pixels, 
                  Pixel const& xyWindow,
                  string const& keyWord,
                  string const& whichObs);

/**
 * @brief Return a vector of pairs of x-limits for each histogram bin
 * @param nBars Number of histogram bins between xMin and xMax
 * @param xMin Start of Histogram in x
 * @param xMax End of Histogram in x
 * @return vector of pairs of x-limits for each histogram bin
 */
vector< pair< float, float > > getHistogramLimits(int const& nBars,
                                                  float const& xMin,
                                                  float const& xMax);

vector<double> getGaiaG(CSVData const& csvData);

/**
 * @brief Return number of stars per bin
 * @param pixelsIn Vector of pixels for which to calculate the histogram
 * @param xyWindow xyWindow for which to calculate the histogram
 * @param whichOne Name of data set
 * @param keyWord  Key word for which to calculate the histogram
 * @param limits   Vector of pairs of lower and upper limits for each bin 
 *
vector<int> getHistogram(vector<Pixel> const& pixelsIn,
                         Pixel const& xyWindow,
                         string const& whichOne,
                         string const& keyWord,
                         vector< pair< float, float > > limits);

**
 * @brief
 * @param 
 *
void makeHistogram(vector<Pixel> const& pixelsIn,
                   Pixel const& xyWindow,
                   string const& whichOne,
                   string const& keyWord,
                   int const& nBars,
                   float const& xMin,
                   float const& xMax,
                   string const& outFileName);
*/
#endif
