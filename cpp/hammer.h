#ifndef __HAMMER_H__
#define __HAMMER_H__

#include <algorithm>
#include <iostream>
#include <math.h>
//#include <mgl2/mgl.h>
#include <stdexcept>
#include <vector>

#define PI 3.14159265
//#define __PLOT__

using namespace std;

/**
 * @brief Structure for x and y coordinates
 */
struct XY{
    double x;
    double y;

    XY() : x(0.0), y(0.0){}
    XY(double a, double b): x(a), y(b){}

//    double getX() const {return x;}
//    double getY() const {return y;}

//    void setX(double xIn){x=xIn;}
//    void setY(double yIn){y=yIn;}
};

/**
 * @brief Structure for pixels in x and y
 */
struct Pixel{
    double xLow;
    double xHigh;
    double yLow;
    double yHigh;

    /**
     * @brief Check if xy is inside pixel
     * @param pixel Pixel to check if xy position is inside
     * @param xy    XY position to check if it is inside pixel
     */
    bool isInside(XY const& xy) const{
//        classInvariant();
        if ((xy.x >= xLow) && (xy.x < xHigh) && (xy.y >= yLow) && (xy.y < yHigh))
            return true;
        return false;
    }

    bool classInvariant() const{
        if (xLow >= xHigh)
            throw std::invalid_argument( "Pixel::classInvariant: ERROR: xLow(="
                    + to_string(xLow) + ") >= xHigh(=" + to_string(xHigh) + ")" );
        if (yLow >= yHigh)
            throw std::invalid_argument( "Pixel::classInvariant: ERROR: yLow(="
                    + to_string(yLow) + ") >= yHigh(=" + to_string(yHigh) + ")" );
        return true;
    }
};

/**
 * @brief Structure for Galactic Longitude and Latitude
 */
struct LonLat{
    double lon;
    double lat;
    
    LonLat() : lon(0.0), lat(0.0){}
    LonLat(double l, double b): lon(l), lat(b){}
};

struct LonLatXY{
    LonLat lonLat;
    XY xy;
};

class Hammer{
public:
    /**
     * @brief Standard Constructor
     * @param deg
     * @return 
     */
    Hammer()
      : _OuterLimits(2*1800+2),
        _OuterLimitsXY(2),
        _NPixX(320),
        _NPixY(160),
        _LonLimit(179.99999),
        _LatLimit(89.99999),
        _KeyWordHammerX("hammerX"),
        _KeyWordHammerY("hammerY"),
        Debug_isInside(false)
    {}

    ~Hammer(){}

    /**
     * @brief Helper function for Hammer projection
     * @param x Hammer x
     * @param y Hammer y
     * @return Hammer z
     */
    double hammerZ(const double& x, const double& y) const{
        return sqrt(1.0 - (x*x / 16.0) - (y*y / 4.0));
    }

    /**
     * @brief Calculate the outer limits in x and y of the Hammer projection
     * @return Vector containing the outer limits (lon=-180, lon=180)
     */
    void calcOuterLimits();

    /**
     * @brief Check if a x-y coordinate is inside the outer limits
     * @param x x-coordinate
     * @param y y-coordinate
     */
    bool isInside(double x, double y);

    bool isInside(XY const& xy){
        return isInside(xy.x, xy.y);
    }

    bool isInside(Pixel const& pix, double const x, double const y) const;

    bool isInside(Pixel const& pix, XY const& xy) const;

    /**
     * @brief Plot the grid of longitudes and latitudes in Hammer projection
     * @param plotName Name for the file to write
     */
//    void plotGrid(string plotName="") const;

    /**
     * @brief return pixels within outer Hammer sphere limits
     */
    vector<Pixel> getPixels();

    /**
     * @brief Convert longitude and latitude to the Hammer Projection x and y
     * @param lon Galactic Longitude in degrees to convert to Hammer x and y
     * @param lat Galactic Latitude in degrees to convert to Hammer x and y
     * @return Hammer x and y
     */
    XY lonLatToXY(const double& lonDeg, const double& latDeg) const;
    XY lonLatToXY(const LonLat& lonLat) const{
        return lonLatToXY(lonLat.lon, lonLat.lat);
    }
    vector< vector< double > > lonLatToXY(vector<double> & lonDeg, vector<double> & latDeg) const;

    /**
     * @brief Convert the Hammer Projection x and y to longitude and latitude
     * @param x Hammer x
     * @param y Hammer y
     * @return Galactic Longitude and Galactic Latitude in degrees
     */
    LonLat xYToLonLat(const double& x, const double& y) const;

//    void plot(vector<LonLatXY> const& lonLatXY, mglGraph& gr, string const& plotName="") const;

    /**
     * @brief Convert degrees to radians
     * @param deg Degrees to convert to radians
     * @return deg in radians
     */
    double rad(const double& deg) const{
        return deg * PI / 180.0;
    }

    /**
     * @brief Convert radians to degrees
     * @param rad Radians to convert to degrees
     * @return rad in degrees
     */
    double deg(const double& rad) const{
        return rad * 180.0 / PI;
    }

    vector<LonLatXY> getOuterLimits();
    vector<XY> getOuterLimitsXY();
    bool getDebug_isInside() const{return Debug_isInside;}

    void setDebug_isInside(bool const setDebug){Debug_isInside = setDebug;}

    string getKeyWordHammerX() const{return _KeyWordHammerX;}
    string getKeyWordHammerY() const{return _KeyWordHammerY;}

private:
    vector<LonLatXY> _OuterLimits;
    vector<XY> _OuterLimitsXY;

    const int _NPixX;
    const int _NPixY;

    const double _LonLimit;
    const double _LatLimit;

    const string _KeyWordHammerX;
    const string _KeyWordHammerY;
    
    bool Debug_isInside;

};
#endif
