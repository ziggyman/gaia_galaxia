#ifndef __GALCOMP_H__
#define __GALCOMP_H__

#include "hammer.h"

using namespace std;

_NPixX = 320;
_NPixY = 160;

vector<Pixel> getPixels(){
    calcOuterLimits();
    vector<Pixel> pixels(0);
    pixels.reserve(320*160);
    Pixel pix;
    double xStep = (_OuterLimitsXY[1].x-_OuterLimitsXY[0].x)/_NPixX;
    double yStep = (_OuterLimitsXY[1].y-_OuterLimitsXY[0].y)/_NPixY;
    for (int xPosLeft=_OuterLimitsXY[0].x; xPosLeft<_OuterLimitsXY[1].x; xPosLeft+=xStep){
        for (int yPosBottom=_OuterLimitsXY[0].y; yPosBottom<_OuterLimitsXY[1].y; yPosBottom+=yStep){
            pix.xLow = xPosLeft;
            pix.xHigh = xPosLeft + xStep;
            pix.yLow = yPosBottom;
            pix.yHigh = yPosBottom + yStep;
            pixels.push_back(pix);
        }
    }
    return pixels;
}

void countStars(string const& dir, string const& fileNameRoot, bool zeroToThreeSixty){
    vector<Pixel> pixels = getPixels();
    
}

void main(){

}
#endif
