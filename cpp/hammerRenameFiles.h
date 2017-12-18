#ifndef __HAMMERRENAMEFILES_H__
#define __HAMMERRENAMEFILES_H__

#include <algorithm>
#include <fstream>
#include <iostream>
#include <math.h>
#include <stdio.h>
#include <vector>
#include "hammer.h"

#define PI 3.14159265
#define __PLOT__

#ifdef __PLOT__
#include <mgl2/mgl.h>
#endif

using namespace std;

vector<LonLatXY> _OuterLimitsIncluded;
vector<XY> _OuterLimitsIncludedXY(2);

XY lonLatToXYWithLimits(const double& lonDeg, const double& latDeg){
    XY xy;

    /// convert lonDeg and latDeg to radians
    double lonRad = rad(lonDeg <= 180.0 ? lonDeg : (lonDeg - 360.0));
    double latRad = rad(latDeg);

    /// do the Hammer transformation
    double temp = sqrt(1.0 + (cos(latRad) * cos(lonRad / 2.0)));
    xy.x = 2.0 * sqrt(2.0) * cos(latRad) * sin(lonRad / 2.0) / temp;
    xy.y = sqrt(2.0) * sin(latRad) / temp;
    
    return xy;
}

XY lonLatToXYWithLimits(const LonLat& lonLat){
    return lonLatToXYWithLimits(lonLat.lon, lonLat.lat);
}

void calcOuterLimitsHelper(){
    int size = _OuterLimitsIncluded.size();
    vector<double> outerLimitsX(0);
    vector<double> outerLimitsY(0);
    outerLimitsX.reserve(size);
    outerLimitsY.reserve(size);
    for (int i=0; i<size; ++i){
        outerLimitsX.push_back(_OuterLimitsIncluded[i].xy.x);
        outerLimitsY.push_back(_OuterLimitsIncluded[i].xy.y);
    }
    _OuterLimitsIncludedXY[0].x = *(min_element(outerLimitsX.begin(), outerLimitsX.end()));
    _OuterLimitsIncludedXY[1].x = *(max_element(outerLimitsX.begin(), outerLimitsX.end()));
    _OuterLimitsIncludedXY[0].y = *(min_element(outerLimitsY.begin(), outerLimitsY.end()));
    _OuterLimitsIncludedXY[1].y = *(max_element(outerLimitsY.begin(), outerLimitsY.end()));
    cout << "xMin = " << _OuterLimitsIncludedXY[0].x << ", xMax = " << _OuterLimitsIncludedXY[1].x
         << ", yMin = " << _OuterLimitsIncludedXY[0].y << ", yMax = " << _OuterLimitsIncludedXY[1].y << endl;
#ifdef __PLOT__
    string plotName("/Volumes/external/azuri/data/limits.png");
    mglGraph gr;
    gr.SetMarkSize(0.00001);
    plot(_OuterLimitsIncluded, gr, plotName);
#endif
    return;
}

/**
 * @brief Calculate the outer limits (including the limits in lon and lat) in x and y of the Hammer projection
 * @return Vector containing the outer limits (lon=-180, lon=180)
 */
void calcOuterLimitsWithLimits(){
    LonLatXY lonLatXY;
    if (_OuterLimitsIncluded.size() == 0){
        _OuterLimitsIncluded.reserve(2*1800);
        for (double lon=-180.0; lon <= 180.0; lon += 360.0){
            for (double lat=-90.0; lat <= 90.0; lat += 0.1){
                lonLatXY.lonLat.lon = lon;
                lonLatXY.lonLat.lat = lat;
                lonLatXY.xy = lonLatToXYWithLimits(lon, lat);
                _OuterLimitsIncluded.push_back(lonLatXY);
//                cout << "calcOuterLimits: lon = " << lon << ", lat = " << lat << ", x = " << lonLatXY.xy.x << ", y = " << lonLatXY.xy.y << endl;
            }
        }
    }
    calcOuterLimitsHelper();
}

/**
 * @brief Check if a x-y coordinate is inside the outer limits
 * @param x x-coordinate
 * @param y y-coordinate
 */
bool isInsideWithLimits(double x, double y){
    if (_OuterLimitsIncluded.size() == 0)
        calcOuterLimitsWithLimits();
    if ((x < _OuterLimitsIncludedXY[0].x) || (x > _OuterLimitsIncludedXY[1].x)){
        if (Debug_isInside)
            cout << "x < _OuterLimitsIncludedXY[0].x) || (x > _OuterLimitsIncludedXY[1].x" << endl;
        return false;
    }
    if ((y < _OuterLimitsIncludedXY[0].y) || (y > _OuterLimitsIncludedXY[1].y)){
        if (Debug_isInside)
            cout << "(y < _OuterLimitsIncludedXY[0].y) || (y > _OuterLimitsIncludedXY[1].y)" << endl;
        return false;
    }
    for (auto itPix=_OuterLimitsIncluded.begin(); itPix!=_OuterLimitsIncluded.end()-1; ++itPix){
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

bool isInsideWithLimits(XY const& xy){
    return isInsideWithLimits(xy.x, xy.y);
}

/**
 * @brief return pixels within outer Hammer sphere limits
 */
vector<Pixel> getPixelsWithLimits(){
    /// running calcOuterLimits()
    calcOuterLimitsWithLimits();

    vector<Pixel> pixels(0);
    pixels.reserve(_NPixX*_NPixY);
    Pixel pix;
    double xStep = (_OuterLimitsIncludedXY[1].x-_OuterLimitsIncludedXY[0].x)/_NPixX;
    double yStep = (_OuterLimitsIncludedXY[1].y-_OuterLimitsIncludedXY[0].y)/_NPixY;
    for (double xPosLeft=_OuterLimitsIncludedXY[0].x; xPosLeft<_OuterLimitsIncludedXY[1].x; xPosLeft+=xStep){
        for (double yPosBottom=_OuterLimitsIncludedXY[0].y; yPosBottom<_OuterLimitsIncludedXY[1].y; yPosBottom+=yStep){
            pix.xLow = xPosLeft;
            pix.xHigh = xPosLeft + xStep;
            pix.yLow = yPosBottom;
            pix.yHigh = yPosBottom + yStep;
            if (isInsideWithLimits(pix.xLow, pix.yLow) || isInsideWithLimits(pix.xLow, pix.yHigh) ||
                isInsideWithLimits(pix.yHigh, pix.yLow) || isInsideWithLimits(pix.xHigh, pix.yHigh)){
                pixels.push_back(pix);
            }
        }
    }
    return pixels;
}

void renameFiles(){

    string dataDir("/Volumes/external/azuri/data/gaia/lon-lat/");
    boost::format fileNameRoot = boost::format("GaiaSource_%i-%i_%i-%i.csv");// % (int(minLongitude), int(maxLongitude), int(minLatitude), int(maxLatitude))

    string dataDirOut("/Volumes/external/azuri/data/gaia/xy/");
    boost::format fileNameOutRoot = boost::format("GaiaSource_%06f-%06f_%06f-%06f.csv");// % (float(minX), float(maxX), float(minY), float(maxY))

    cout << "running calcOuterLimits" << endl;
    calcOuterLimitsWithLimits();

    cout << "running getPixels" << endl;
    vector<Pixel> pixelsWithLimits=getPixelsWithLimits();
    vector<Pixel> pixelsWithoutLimits=getPixels();
    if (pixelsWithLimits.size() != pixelsWithoutLimits.size()){
        cout << "ERROR: pixelsWithLimits.size()(=" << pixelsWithLimits.size() << ") != pixelsWithoutLimits.size()(=" << pixelsWithoutLimits.size() << ")" << endl;
        exit(EXIT_FAILURE);
    }
    for (int iPix=0; iPix<pixelsWithLimits.size(); ++iPix){
        cout << "pixelsWithLimits: iPix=" << iPix << ": pix.xLow=" << pixelsWithoutLimits[iPix].xLow << ", pix.xHigh=" << pixelsWithoutLimits[iPix].xHigh << ", pix.yLow=" << pixelsWithoutLimits[iPix].yLow << ", pix.yHigh=" << pixelsWithoutLimits[iPix].yHigh << endl;
        cout << "pixelsWithLimits: iPix=" << iPix << ": pixWL.xLow=" << pixelsWithLimits[iPix].xLow << ", pixWL.xHigh=" << pixelsWithLimits[iPix].xHigh << ", pixWL.yLow=" << pixelsWithLimits[iPix].yLow << ", pixWL.yHigh=" << pixelsWithLimits[iPix].yHigh << endl;
    }

    cout << "creating vectors for longitudes and latitudes" << endl;
    vector<int> longitudes(0);
    vector<int> latitudes(0);
    for (int lon=0; lon<=360; lon+=10)
        longitudes.push_back(lon);
    for (int lat=-90; lat<=90; lat+=10)
        latitudes.push_back(lat);

    ///create vectors of outFileNames
    for (int iPix=0; iPix<pixelsWithLimits.size(); ++iPix){
        string outFileNameWithLimits = dataDirOut + (fileNameOutRoot % pixelsWithLimits[iPix].xLow
                                                                     % pixelsWithLimits[iPix].xHigh
                                                                     % pixelsWithLimits[iPix].yLow
                                                                     % pixelsWithLimits[iPix].yHigh).str();
        string outFileNameWithoutLimits = dataDirOut + (fileNameOutRoot % pixelsWithoutLimits[iPix].xLow
                                                                     % pixelsWithoutLimits[iPix].xHigh
                                                                     % pixelsWithoutLimits[iPix].yLow
                                                                     % pixelsWithoutLimits[iPix].yHigh).str();
        if (outFileNameWithLimits.compare(outFileNameWithoutLimits) != 0){
            if (!ifstream(outFileNameWithLimits)){
                cout << "outFileNameWithLimits not found" << endl;
                exit(EXIT_FAILURE);
            }
            else{
                cout << "Renaming <" << outFileNameWithLimits << "> to <" << outFileNameWithoutLimits << ">" << endl;
                rename(outFileNameWithLimits.c_str(), outFileNameWithoutLimits.c_str());
////                  rename(outFileNameWithoutLimits.c_str(), outFileNameWithLimits.c_str());
            }
        }
    }
    return;
}

#endif
