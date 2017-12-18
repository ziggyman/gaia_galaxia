#include "hammer.h"

XY Hammer::lonLatToXY(const double& lonDeg, const double& latDeg){
    XY xy;

    /// The exact outer limits are not supported by the Hammer transformation,
    /// so if lonDeg or latDeg are exactly at the outer limits, we push them inside
    double lon(lonDeg);
    if ((lon > _LonLimit) && (lon <= 180.0))
        lon = _LonLimit;
    else if ((lon < 0.0-_LonLimit) && (lon >= -180.0))
        lon = 0.0-_LonLimit;
    else if (lon > 180.0)
        lon -= 360.0;

    double lat(latDeg);
    if ((lat > _LatLimit) && (lat <= 90.0))
        lat = _LatLimit;
    else if ((lat < 0.0-_LatLimit) && (lat >= -90.0))
        lat = 0.0-_LatLimit;

    /// convert lonDeg and latDeg to radians
    double lonRad = rad(lon);
    double latRad = rad(lat);

    /// do the Hammer transformation
    double temp = sqrt(1.0 + (cos(latRad) * cos(lonRad / 2.0)));
    xy.x = 2.0 * sqrt(2.0) * cos(latRad) * sin(lonRad / 2.0) / temp;
    xy.y = sqrt(2.0) * sin(latRad) / temp;

    return xy;
}

LonLat Hammer::xYToLonLat(const double& x, const double& y){
    LonLat lonLat;
    double z = hammerZ(x, y);
    lonLat.lon = deg(2.0 * atan(z * x / (2.0 * (2.0 * z * z - 1.0))));
    lonLat.lat = deg(asin(z * y));
    return lonLat;
}


void Hammer::plot(vector<LonLatXY> const& lonLatXY, mglGraph& gr, string const& plotName){
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
void Hammer::calcOuterLimits(){
    LonLatXY lonLatXY;
    if (_OuterLimits[0].lonLat.lon == 0.0){
        int pos=0;
        for (double lon=-180.0; lon <= 180.0; lon += 360.0){
            for (double lat=-90.0; lat <= 90.0; lat += 0.1){
                lonLatXY.lonLat.lon = lon;
                lonLatXY.lonLat.lat = lat;
                lonLatXY.xy = lonLatToXY(lon, lat);
                _OuterLimits[pos] = lonLatXY;
//                cout << "calcOuterLimits: lon = " << lon << ", lat = " << lat << ", x = " << lonLatXY.xy.x << ", y = " << lonLatXY.xy.y << endl;
                ++pos;
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
    cout << "xMin = " << _OuterLimitsXY[0].x << ", xMax = " << _OuterLimitsXY[1].x
         << ", yMin = " << _OuterLimitsXY[0].y << ", yMax = " << _OuterLimitsXY[1].y << endl;
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
bool Hammer::isInside(double x, double y){
    if (_OuterLimits.size() == 0)
        calcOuterLimits();
    if ((x < _OuterLimitsXY[0].x) || (x > _OuterLimitsXY[1].x)){
        if (Debug_isInside)
            cout << "x < _OuterLimitsXY[0].x) || (x > _OuterLimitsXY[1].x" << endl;
        return false;
    }
    if ((y < _OuterLimitsXY[0].y) || (y > _OuterLimitsXY[1].y)){
        if (Debug_isInside)
            cout << "(y < _OuterLimitsXY[0].y) || (y > _OuterLimitsXY[1].y)" << endl;
        return false;
    }
    for (auto itPix=_OuterLimits.begin(); itPix!=_OuterLimits.end()-1; ++itPix){
        Pixel pixel;
        auto itNext = itPix+1;
        pixel.xLow = itPix->xy.x < itNext->xy.x ? itPix->xy.x : itNext->xy.x;
        pixel.xHigh = itPix->xy.x > itNext->xy.x ? itPix->xy.x : itNext->xy.x;
        pixel.yLow = itPix->xy.y < itNext->xy.y ? itPix->xy.y : itNext->xy.y;
        pixel.yHigh = itPix->xy.y > itNext->xy.y ? itPix->xy.y : itNext->xy.y;
        if (((x < 0.0) && (x >= pixel.xLow)) || ((x >= 0.0) && (x <= pixel.xHigh))){
            if (Debug_isInside){
                cout << "x=" << x << " is inside [" << pixel.xLow << ", " << pixel.xHigh << "]" << endl;
            }
            if (((y < 0.0) && (y >= pixel.yLow)) || ((y >= 0.0) && (y <= pixel.yHigh))){
                if (Debug_isInside){
                    cout << "y=" << y << " is inside [" << pixel.yLow << ", " << pixel.yHigh << "]" << endl;
                }
                return true;
            }
            else{
                if (Debug_isInside){
                    cout << "y=" << y << " is outside [" << pixel.yLow << ", " << pixel.yHigh << "]" << endl;
                }
            }
        }
    }
    if (Debug_isInside)
        cout << "x(=" << x << "), y(=" << y << ") not found to be inside a pixel" << endl;
    return false;
}

bool Pixel::isInside(XY const& xy){
    if ((xy.x >= xLow) && (xy.x < xHigh) && (xy.y >= yLow) && (xy.y < yHigh))
        return true;
    return false;
}

void Hammer::plotGrid(string plotName){
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

vector<Pixel> Hammer::getPixels(){
    /// running calcOuterLimits()
    calcOuterLimits();

    vector<Pixel> pixels(0);
    pixels.reserve(_NPixX*_NPixY);
    Pixel pix;
    double xStep = (_OuterLimitsXY[1].x-_OuterLimitsXY[0].x)/_NPixX;
    double yStep = (_OuterLimitsXY[1].y-_OuterLimitsXY[0].y)/_NPixY;
    for (double xPosLeft=_OuterLimitsXY[0].x; xPosLeft<_OuterLimitsXY[1].x; xPosLeft+=xStep){
        for (double yPosBottom=_OuterLimitsXY[0].y; yPosBottom<_OuterLimitsXY[1].y; yPosBottom+=yStep){
            pix.xLow = xPosLeft;
            pix.xHigh = xPosLeft + xStep;
            pix.yLow = yPosBottom;
            pix.yHigh = yPosBottom + yStep;
            if (isInside(pix.xLow, pix.yLow) || isInside(pix.xLow, pix.yHigh) ||
                isInside(pix.yHigh, pix.yLow) || isInside(pix.xHigh, pix.yHigh)){
                pixels.push_back(pix);
            }
        }
    }
    return pixels;
}
