#ifndef __GALAXYMATH_H__
#define __GALAXYMATH_H__

#include <cmath>
#include <iostream>
#include <random>
#include <string>
#include <vector>
//#include "csvData.h"

using namespace std;

struct Histogram{
    vector< std::pair< double, double > > limits;/// limit=[limits[i].first, limits[i].second)
    vector< vector< unsigned > > indices;
    double start;
    double end;
    unsigned nBins;

    /**
     * @brief populate limits with each element a pair limit=[limits[i].first, limits[i].second)
     * @param startIn  lower limit of lowest data bin
     * @param endIn    upper limit of highest data bin
     * @param nBinsIn number of bins
     */
    void makeBinLimits(double startIn, double endIn, unsigned nBinsIn);

    /**
     * @brief Populate this->indices with indices of vecIn which fall into step i
     *        which is [limits[i].first, limits[i].second)
     * @param vecIn : data from which to count elements in limits
     */
    template< typename T >
    void make(vector<T> const& vecIn);

    /**
     * @brief Fill a vector of vectors of indices randomly with elements of dataIn
     *        Requires that dataIn has more elements per bin than the original vector
     *        this was constructed from
     */
    template< typename T >
    vector< vector< unsigned > > fillRandomly(vector< T > const& dataIn, unsigned & seed);

    /**
     * @brief convolve data in this with the errors given in errorsObs
     *
    vector< vector< pair< double, double > > > convolveWithObservationErrors(
        vector<double> const& dataIn,
        Histogram const& errorsObs
    );*/
};

/**
 * @brief Return a vector [min, min+step,...,min+n*step<=max]
 */
template< typename T >
vector<T> generateSequence(T min, T max, T step=1);

/*
 * @brief create random sequence of non-repeating integers in [min, max]
 *        If seed is equal to 0 a random seed is created
 */
vector<unsigned> generateRandomSequence(unsigned min, unsigned max, unsigned seed);

/*
 * @brief create random sequence of n<=max-min+1 non-repeating integers in [min, max]
 *        If seed is equal to 0 a random seed is created
 */
vector<unsigned> generateRandomSequence(unsigned min, unsigned max, unsigned n, unsigned seed);

/**
 * @brief convert degree to radian
 */
double degToRad(double deg);

/**
 * @brief convert radian to degree
 */
double radToDeg(double rad);

/**
 * @brief convert proper motions from Equatorial Coordinates ra and dec to Galactic Coordinates l and b
 */
pair<double, double> muRaDecToMuLB(double muRa, double muDec, double ra, double dec);

/**
 * @brief Convert the parallax from mas to distance in kpc
 */
double parallaxToDistance(double par);

#endif
