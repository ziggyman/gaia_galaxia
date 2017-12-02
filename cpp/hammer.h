#ifndef __HAMMER_H__
#define __HAMMER_H__

#define PI 3.14159265

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
    return std::sqrt(1.0 - (x*x / 16.0) - (y*y / 4.0))
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
    float temp = std::sqrt(1.0 + (cos(latRad) * cos(lonRad / 2.0)));
    xy.x = 2.0 * std::sqrt(2.0) * std::cos(latRad) * std::sin(lonRad / 2.0) / temp;
    xy.y = std::sqrt(2.0) * std::sin(latRad) / temp;
    return xy;
}

/**
 * @brief Convert Hammer x and y back to Galactic longitude and latitude
 * @param x Hammer x
 * @param x Hammer y
 * @return LonLat
 */
LonLat xYToLonLat(const float& x, const float& x){
    LonLat lonLat;
    float z = hammerZ(x, y);
    lonLat.lon = deg(2.0 * std::atan(z * x / (2.0 * (2.0 * z * z - 1.0))));
    lonLat.lat = deg(std::asin(z * y));
    return lonLat;
}

#endif
