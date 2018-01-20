#include "parameters.h"

boost::format galaxiaGetFileNameOutRoot(){
    return boost::format("galaxia_%06f-%06f_%06f-%06f.csv");// % (float(minX), float(maxX), float(minY), float(maxY))
}

boost::format gaiaGetFileNameOutRoot(){
    return boost::format("GaiaSource_%06f-%06f_%06f-%06f.csv");// % (float(minX), float(maxX), float(minY), float(maxY))
}

boost::format gaiaTgasGetFileNameOutRoot(){
    return boost::format("TgasSource_%06f-%06f_%06f-%06f.csv");// % (float(minX), float(maxX), float(minY), float(maxY))
}

string galaxiaGetDataDirOut(){
//    return "/Volumes/yoda/azuri/data/galaxia/xy/";
    return "/Volumes/yoda/azuri/data/galaxia/xy1/";
}

string gaiaGetDataDirOut(){
    return "/Volumes/external/azuri/data/gaia/xy/";
}

string gaiaTgasGetDataDirOut(){
    return "/Volumes/yoda/azuri/data/gaia-tgas/xy/";
}
