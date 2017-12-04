#ifndef __GALCOMP_H__
#define __GALCOMP_H__

#include "hammer.h"

using namespace std;

_NPixX = 320;
_NPixY = 160;

/**
 * @brief return pixels _NPixX * _NPixY
 */
vector<Pixel> getPixels();

void countStars(string const& dir, string const& fileNameRoot, bool zeroToThreeSixty){
    vector<Pixel> pixels = getPixels();
    
}

void main(){

}
#endif
