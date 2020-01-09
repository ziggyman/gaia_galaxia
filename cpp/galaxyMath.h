#ifndef __GALAXYMATH_H__
#define __GALAXYMATH_H__

#include <algorithm>
#include <cmath>
#include <iostream>
#include <random>
#include <string>
#include <vector>

using namespace std;

//struct ApparentMagnitudeResult{
//    double appMag;
//    string flag;
//};

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
 * @brief convert Ra and Dec to l and b
 * @param ra
 * @param dec
 * @return 
 */
pair<double, double> raDecToLB(double ra, double dec);

/**
 * @brief convert proper motions from Equatorial Coordinates ra and dec to Galactic Coordinates l and b
 */
pair<double, double> muRaDecToMuLB(double muRa, double muDec, double ra, double dec);

/**
 * @brief Convert the parallax from mas to distance in kpc
 */
double parallaxToDistance(double par);
vector<double> parallaxToDistance(vector<double> const& par);

double calcGaiaGFromgri(double const& sdss_g, double const& sdss_r, double const& sdss_i);
vector<double> calcGaiaGFromgri(vector<double> const& sdss_g,
                                vector<double> const& sdss_r,
                                vector<double> const& sdss_i);

double calcIcFromBVg(double const& ubv_b, double const& ubv_v, double const& g);
vector<double> calcIcFromBVg(vector<double> const& ubv_b,
                             vector<double> const& ubv_v,
                             vector<double> const& g);

double calcGaiaGFromVI(double const& ubv_v, double const& ubv_i);
vector<double> calcGaiaGFromVI(vector<double> const& ubv_v, vector<double> const& ubv_i);

double calcGaiaGFromBVI(double const& ubv_b, double const& ubv_v, double const& ubv_i);
vector<double> calcGaiaGFromBVI(vector<double> const& ubv_b, vector<double> const& ubv_v, vector<double> const& ubv_i);

/**
 * @brief Calculate a - b
 * @param a : a
 * @param b : b
 * @return : a - b
 */
template<typename T>
vector<T> difference(vector<T> const& a, vector<T> const& b);

/**
 * @brief Calculate a_i - b
 * @param a : a
 * @param b : b
 * @return : a - b
 */
template<typename T>
vector<T> difference(vector<T> const& a, T const& b);

/**
 * @brief Calculate sum of elements in a
 * @param a : a
 * @return : sum(a)
 */
template< typename T >
T sum(vector< T > const& a);

/**
 * @brief Calculate mean(a)
 * @param a : a
 * @return : mean(a)
 */
template<typename T>
T mean(vector<T> const& a);

/**
 * @brief Calculate the variance of a
 * @param a : a
 * @return : variance of a
 */
template< typename T >
T variance(vector< T > const& a);

/**
 * @brief Calcualte the Standard Deviation of a
 * @param a : a
 * @return : standard deviation of a
 */
template< typename T >
T standardDeviation(vector< T > const& a);

/**
 * @brief : calculate a_i ^ n
 * @param a : a
 * @param n : n
 * @return : [a_i ^ n]
 */
template< typename T >
vector< T > pow(vector< T > const& a, int n);

/**
 * @brief : return a [X,Y,Z] unit vector in ICRS Coordinates from Right ascension alpha
 *          and Declination delta
 * @param alpha : Right ascension
 * @param delta : declination
 * @return : [X_ICRS, Y_ICRS, Z_ICRS] of unit length
 */
template< typename T >
vector< T > getICRSUnitVector(T const& alpha, T const& delta );
//vector< double > getICRSUnitVector(double const& alpha, double const& delta );

/**
 * @brief : return a [X,Y,Z] unit vector in Galactic Coordinates from Galactic Longitude l
 *          and Galactic Latitude b
 * @param l : Galactic longitude
 * @param b : Galactic latitude
 * @return : [X_Gal, Y_Gal, Z_Gal] of unit length
 */
template< typename T >
vector< T > getGalUnitVector(T const& l, T const& b );

#endif
