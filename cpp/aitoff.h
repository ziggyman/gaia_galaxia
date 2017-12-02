#ifndef __AITOFF_H__
#define __AITOFF_H__

struct XY{
    float x;
    float y;
};

struct LonLat{
    float lon;
    float lat;
};

float sinc(const float& x){
    if (x == 0.0)
        return 1.0;
    return std::sin(x) / x;
}

XY lonLatToXY(const float& lon, const float& lat){
    XY xy;
    float alpha = std::acos(std::cos(lat) * std::cos(lon/2.0));
    XY.x = (2.0 * std::cos(lat) * std::sin(lon / 2.0)) / sinc(alpha);
    XY.y = std::sin(lat) / sinc(alpha);
    return xy;
}

float xYToLonLat(const float& x, const float& x){

}

#endif
