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
    float x;
    float y;
};

/**
 * @brief Structure for Galactic Longitude and Latitude
 */
struct LonLat{
    float lon;
    float lat;
};

struct LonLatXY{
    LonLat lonLat;
    XY xy;
};

/**
 * @brief Convert degrees to radians
 * @param deg Degrees to convert to radians
 * @return deg in radians
 */
float rad(const float& deg){
    return deg * PI / 180.0;
}

/**
 * @brief Convert radians to degrees
 * @param rad Radians to convert to degrees
 * @return rad in degrees
 */
float deg(const float& rad){
    return rad * 180.0 / PI;
}

/**
 * @brief Helper function for Hammer projection
 * @param x Hammer x
 * @param y Hammer y
 * @return Hammer z
 */
float hammerZ(const float& x, const float& y){
    return sqrt(1.0 - (x*x / 16.0) - (y*y / 4.0));
}

/**
 * @brief Convert lon and lat the Hammer Projection x and y
 * @param lon Galactic Longitude to convert to Hammer x and y
 * @param lat Galactic Latitude to convert to Hammer x and y
 * @return Hammer x and y
 */
XY lonLatToXY(const float& lon, const float& lat){
    XY xy;
    float lonRad = rad(lon);
    float latRad = rad(lat);
    float temp = sqrt(1.0 + (cos(latRad) * cos(lonRad / 2.0)));
    xy.x = 2.0 * sqrt(2.0) * cos(latRad) * sin(lonRad / 2.0) / temp;
    xy.y = sqrt(2.0) * sin(latRad) / temp;
    return xy;
}

/**
 * @brief Convert Hammer x and y back to Galactic longitude and latitude
 * @param x Hammer x
 * @param x Hammer y
 * @return LonLat
 */
LonLat xYToLonLat(const float& x, const float& y){
    LonLat lonLat;
    float z = hammerZ(x, y);
    lonLat.lon = deg(2.0 * atan(z * x / (2.0 * (2.0 * z * z - 1.0))));
    lonLat.lat = deg(asin(z * y));
    return lonLat;
}

/**
 * @brief Calculate the outer limits in x and y of the Hammer projection
 * @return Vector containing the outer limits (lon=0, lon=360)
 */
vector<LonLatXY> getOuterLimits(){
    LonLatXY lonLatXY;
    vector<LonLatXY> out;
    out.reserve(2*180);
    for (float lon=-180.0; lon <= 180.0; lon += 360.0){
        for (float lat=-90.0; lat <= 90.0; lat += 1.0){
            lonLatXY.lonLat.lon = lon;
            lonLatXY.lonLat.lat = lat;
            lonLatXY.xy = lonLatToXY(lon, lat);
            out.push_back(lonLatXY);
        }
    }
#ifdef __PLOT__
    string plotName("/Volumes/external/azuri/data/limits.png");
    mglGraph gr;
    gr.Title("Hammer sphere");
    gr.Box();
//    gr.SetMarkSize(0.1);
    vector<double> xs(0);
    xs.reserve(out.size());
    vector<double> ys(0);
    ys.reserve(out.size());
    for (int i=0; i<out.size(); ++i){
        xs.push_back(out[i].xy.x);
        ys.push_back(out[i].xy.y);
    }
    mglData MGLData_X;
    MGLData_X.Link(xs.data(), xs.size(), 0, 0);
    mglData MGLData_Y;
    MGLData_Y.Link(ys.data(), ys.size(), 0, 0);
    double minX = *(min_element(xs.begin(), xs.end()));
    double maxX = *(max_element(xs.begin(), xs.end()));
    double minY = *(min_element(ys.begin(), ys.end()));
    double maxY = *(max_element(ys.begin(), ys.end()));
    cout << "minX = " << minX << ", maxX = " << maxX << ", minY = " << minY << ", maxY = " << maxY << endl;
    gr.SetRanges(minX,
                 maxX,
                 minY,
                 maxY);
    gr.Axis();
    gr.Label('x',"",0);
    gr.Label('y',"",0);
    gr.Plot(MGLData_X, MGLData_Y, " +");
    gr.WriteFrame(plotName.c_str());

#endif
    return out;
}

#endif
