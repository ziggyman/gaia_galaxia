#ifndef __HAMMER_H__
#define __HAMMER_H__

#include <algorithm>
#include <iostream>
#include <math.h>
#include <vector>

#define PI 3.14159265
#define __PLOT__

#ifdef __PLOT__
#include <mgl2/mgl.h>
#endif

using namespace std;
/**
 * @brief Structure for x and y coordinates
 */
struct XY{
    double x;
    double y;
};

/**
 * @brief Structure for pixels in x and y
 */
struct Pixel{
    double xLow;
    double xHigh;
    double yLow;
    double yHigh;
};

/**
 * @brief Structure for Galactic Longitude and Latitude
 */
struct LonLat{
    double lon;
    double lat;
};

struct LonLatXY{
    LonLat lonLat;
    XY xy;
};

vector<LonLatXY> _OuterLimits;
vector<XY> _OuterLimitsXY(2);

int _NPixX = 320;
int _NPixY = 160;

/**
 * @brief Convert degrees to radians
 * @param deg Degrees to convert to radians
 * @return deg in radians
 */
double rad(const double& deg){
    return deg * PI / 180.0;
}

/**
 * @brief Convert radians to degrees
 * @param rad Radians to convert to degrees
 * @return rad in degrees
 */
double deg(const double& rad){
    return rad * 180.0 / PI;
}

/**
 * @brief Helper function for Hammer projection
 * @param x Hammer x
 * @param y Hammer y
 * @return Hammer z
 */
double hammerZ(const double& x, const double& y){
    return sqrt(1.0 - (x*x / 16.0) - (y*y / 4.0));
}

/**
 * @brief Convert longitude and latitude to the Hammer Projection x and y
 * @param lon Galactic Longitude in degrees to convert to Hammer x and y
 * @param lat Galactic Latitude in degrees to convert to Hammer x and y
 * @return Hammer x and y
 */
XY lonLatToXY(const double& lonDeg, const double& latDeg){
    XY xy;
    double lonRad = rad(lonDeg);
    double latRad = rad(latDeg);
    double temp = sqrt(1.0 + (cos(latRad) * cos(lonRad / 2.0)));
    xy.x = 2.0 * sqrt(2.0) * cos(latRad) * sin(lonRad / 2.0) / temp;
    xy.y = sqrt(2.0) * sin(latRad) / temp;
    return xy;
}

XY lonLatToXY(const LonLat& lonLat){
    return lonLatToXY(lonLat.lon, lonLat.lat);
}

/**
 * @brief Convert Hammer x and y back to Galactic longitude and latitude in degrees
 * @param x Hammer x
 * @param x Hammer y
 * @return LonLat in degrees
 */
LonLat xYToLonLat(const double& x, const double& y){
    LonLat lonLat;
    double z = hammerZ(x, y);
    lonLat.lon = deg(2.0 * atan(z * x / (2.0 * (2.0 * z * z - 1.0))));
    lonLat.lat = deg(asin(z * y));
    return lonLat;
}


void plot(vector<LonLatXY> const& lonLatXY, mglGraph& gr, string const& plotName=""){
    gr.Title("Hammer sphere");
    gr.Box();
    vector<double> xs(0);
    xs.reserve(lonLatXY.size());
    vector<double> ys(0);
    ys.reserve(lonLatXY.size());
    for (int i=0; i<lonLatXY.size(); ++i){
        xs.push_back(lonLatXY[i].xy.x);
        ys.push_back(lonLatXY[i].xy.y);
    }
    mglData MGLData_X;
    MGLData_X.Link(xs.data(), xs.size(), 0, 0);
    mglData MGLData_Y;
    MGLData_Y.Link(ys.data(), ys.size(), 0, 0);
    double minX = *(min_element(xs.begin(), xs.end()));
    double maxX = *(max_element(xs.begin(), xs.end()));
    double minY = *(min_element(ys.begin(), ys.end()));
    double maxY = *(max_element(ys.begin(), ys.end()));
    gr.SetRanges(minX,
                 maxX,
                 minY,
                 maxY);
    gr.Axis();
    gr.Label('x',"",0);
    gr.Label('y',"",0);
    gr.SetSize(4096, 2024);
    gr.Plot(MGLData_X, MGLData_Y, " *");
    if (plotName.compare("") != 0)
        gr.WriteFrame(plotName.c_str());
    return;
}

/**
 * @brief Calculate the outer limits in x and y of the Hammer projection
 * @return Vector containing the outer limits (lon=-180, lon=180)
 */
void calcOuterLimits(){
    LonLatXY lonLatXY;
    if (_OuterLimits.size() == 0){
        _OuterLimits.reserve(2*180);
        for (double lon=-180.0; lon <= 180.0; lon += 360.0){
            for (double lat=-90.0; lat < 90.0; lat += 0.1){
                lonLatXY.lonLat.lon = lon;
                lonLatXY.lonLat.lat = lat;
                lonLatXY.xy = lonLatToXY(lon, lat);
                _OuterLimits.push_back(lonLatXY);
            }
        }
    }
    int size = _OuterLimits.size();
    vector<double> outerLimitsX(0);
    vector<double> outerLimitsY(0);
    outerLimitsX.reserve(size);
    outerLimitsY.reserve(size);
    for (int i=0; i<size; ++i){
        outerLimitsX.push_back(_OuterLimits[i].xy.x);
        outerLimitsY.push_back(_OuterLimits[i].xy.y);
    }
    _OuterLimitsXY[0].x = *(min_element(outerLimitsX.begin(), outerLimitsX.end()));
    _OuterLimitsXY[1].x = *(max_element(outerLimitsX.begin(), outerLimitsX.end()));
    _OuterLimitsXY[0].y = *(min_element(outerLimitsY.begin(), outerLimitsY.end()));
    _OuterLimitsXY[1].y = *(max_element(outerLimitsY.begin(), outerLimitsY.end()));
//    cout << "xMin = " << _OuterLimitsXY[0].x << ", xMax = " << _OuterLimitsXY[1].x
//         << ", yMin = " << _OuterLimitsXY[0].y << ", yMax = " << _OuterLimitsXY[1].y << endl;
#ifdef __PLOT__
    string plotName("/Volumes/external/azuri/data/limits.png");
    mglGraph gr;
    gr.SetMarkSize(0.00001);
    plot(_OuterLimits, gr, plotName);
#endif
    return;
}

/**
 * @brief Check if a x-y coordinate is inside the outer limits
 * @param x x-coordinate
 * @param y y-coordinate
 */
bool isInside(double x, double y){
    if (_OuterLimits.size() == 0)
        calcOuterLimits();
    if ((x < _OuterLimitsXY[0].x) || (x > _OuterLimitsXY[1].x))
        return false;
    if ((y < _OuterLimitsXY[0].y) || (y > _OuterLimitsXY[1].y))
        return false;
    LonLat lonLatZero = xYToLonLat(0.0, y);
    XY xyLeft = lonLatToXY(-179.99999, lonLatZero.lat);
    XY xyRight = lonLatToXY(179.99999, lonLatZero.lat);
    if ((x < xyLeft.x) || (x > xyRight.x))
        return false;
    return true;
}

/**
 * @brief Check if xy is inside pixel
 * @param pixel Pixel to check if xy position is inside
 * @param xy    XY position to check if it is inside pixel
 */
bool isInPixel(Pixel const& pixel, XY const& xy){
    if ((xy.x >= pixel.xLow) && (xy.x < pixel.xHigh) && (xy.y >= pixel.yLow) && (xy.y < pixel.yHigh))
        return true;
    return false;
}

/**
 * @brief Plot the grid of longitudes and latitudes in Hammer projection
 * @param plotName Name for the file to write
 */
void plotGrid(string plotName=""){
    mglGraph gr;
    gr.SetMarkSize(0.00001);
    LonLatXY lonLatXY;
    vector<LonLatXY> out;
    out.reserve(180*180);
    for (double lon=-180.0; lon <= 180.0; lon += 10.0){
        for (double lat=-90.0; lat < 90.0; lat += 0.1){
            lonLatXY.lonLat.lon = lon;
            lonLatXY.lonLat.lat = lat;
            lonLatXY.xy = lonLatToXY(lon, lat);
            out.push_back(lonLatXY);
        }
    }
    for (double lon=-180.0; lon <= 180.0; lon += 0.1){
        for (double lat=-90.0; lat < 90.0; lat += 10.0){
            lonLatXY.lonLat.lon = lon;
            lonLatXY.lonLat.lat = lat;
            lonLatXY.xy = lonLatToXY(lon, lat);
            out.push_back(lonLatXY);
        }
    }
    plot(out, gr, plotName);
    return;
}

/**
 * @brief return pixels within outer Hammer sphere limits
 */
vector<Pixel> getPixels(){
//    cout << "getPixels: running calcOuterLimits()" << endl;
    calcOuterLimits();
    vector<Pixel> pixels(0);
    pixels.reserve(320*160);
    Pixel pix;
    double xStep = (_OuterLimitsXY[1].x-_OuterLimitsXY[0].x)/_NPixX;
    double yStep = (_OuterLimitsXY[1].y-_OuterLimitsXY[0].y)/_NPixY;
//    cout << "getPixels: xStep = " << xStep << ", yStep = " << yStep << endl;
//    cout << "getPixels: starting for loop" << endl;
    for (double xPosLeft=_OuterLimitsXY[0].x; xPosLeft<_OuterLimitsXY[1].x; xPosLeft+=xStep){
//        cout << "xPosLeft = " << xPosLeft << endl;
        for (double yPosBottom=_OuterLimitsXY[0].y; yPosBottom<_OuterLimitsXY[1].y; yPosBottom+=yStep){
//            cout << "yPosBottom =  " << yPosBottom << endl;
            pix.xLow = xPosLeft;
            pix.xHigh = xPosLeft + xStep;
            pix.yLow = yPosBottom;
            pix.yHigh = yPosBottom + yStep;
//            cout << "pix.xLow = " << pix.xLow << ", pix.xHigh = " << pix.xHigh << ", pix.yLow = " << pix.yLow << ", pix.yHigh = " << pix.yHigh << endl;
            if (isInside(pix.xLow, pix.yLow) || isInside(pix.xLow, pix.yHigh) ||
                isInside(pix.yHigh, pix.yLow) || isInside(pix.xHigh, pix.yHigh)){
                pixels.push_back(pix);
//                cout << "pix isInside" << endl;
            }
        }
    }
//    cout << "getPixels finished: pixels.size() = " << pixels.size() << endl;
    return pixels;
}

#endif
