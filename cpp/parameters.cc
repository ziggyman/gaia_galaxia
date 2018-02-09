#include "parameters.h"

boost::format modelGetFileNameOutRoot(){
    return boost::format("galaxia_%06f-%06f_%06f-%06f.csv");// % (float(minX), float(maxX), float(minY), float(maxY))
}

boost::format obsGetFileNameOutRoot(string const& whichOne){
    if (whichOne.compare("gaia") == 0)
        return gaiaGetFileNameOutRoot();
    else if (whichOne.compare("gaiaTgas") == 0)
        return gaiaTgasGetFileNameOutRoot();
    else
        throw std::runtime_error("obsGetFileNameOutRoot: ERROR: whichOne = <"+whichOne+"> not recognized");
}

boost::format gaiaGetFileNameOutRoot(){
    return boost::format("GaiaSource_%06f-%06f_%06f-%06f.csv");// % (float(minX), float(maxX), float(minY), float(maxY))
}

boost::format gaiaTgasGetFileNameOutRoot(){
    return boost::format("TgasSource_%06f-%06f_%06f-%06f.csv");// % (float(minX), float(maxX), float(minY), float(maxY))
}

string modelGetDataDirOut(){
    return "/Volumes/yoda/azuri/data/galaxia/xy_ubv_Vlt13/";
//    return "/Volumes/yoda/azuri/data/galaxia/xy1/";
}

string obsGetDataDirOut(string const& whichOne){
    if (whichOne.compare("gaia") == 0)
        return gaiaGetDataDirOut();
    else if (whichOne.compare("gaiaTgas") == 0)
        return gaiaTgasGetDataDirOut();
    else
        throw std::runtime_error("obsGetDataDirOut: ERROR: whichOne = <"+whichOne+"> not recognized");
}

string gaiaGetDataDirOut(){
    return "/Volumes/external/azuri/data/gaia/xy/";
}

string gaiaTgasGetDataDirOut(){
    return "/Volumes/yoda/azuri/data/gaia-tgas/xy/";
}

string obsGetFilter(){
    return "g";
}
string obsGetFilterKeyWord(string const& filter){
    if (filter.compare("g") == 0)
        return "phot_g_mean_mag";
    else
        throw std::runtime_error("obsGetFilterKeyWord: ERROR: unknown filter <"+filter+">");
}

string modelGetFilterKeyWord(string const& filter){
    if (filter.compare("g") == 0)
        return "sdss_g";
    else
        throw std::runtime_error("galaxiaGetFilterKeyWord: ERROR: unknown filter <"+filter+">");
}

string modelGetHeaderKeyWord(string const& keyWord){
    if (keyWord.compare("distance"))///[kpc]
        return "rad";
    else if (keyWord.compare("log_Teff"))
        return "teff";
    else if (keyWord.compare("mu_b"))
        return "mub";
    else if (keyWord.compare("mu_l"))
        return "mul";
    else if (keyWord.compare("FeH"))
        return "feh";
    else if (keyWord.compare("v_rad"))
        return "vrad";
/*    else if (keyWord.compare(""))
        return "";
    else if (keyWord.compare(""))
        return "";
    else if (keyWord.compare(""))
        return "";
    else if (keyWord.compare(""))
        return "";
    else if (keyWord.compare(""))
        return "";*/
    else
        throw std::runtime_error("modelGetHeaderKeyWord: ERROR: unknow keyWord <"+keyWord+">");
}

string obsGetHeaderKeyWord(string const& keyWord){
    if (keyWord.compare("mu_ra"))
        return "pmra";
    else if (keyWord.compare("error_mu_ra"))
        return "pmra_error";
    else if (keyWord.compare("mu_dec"))
        return "pmdec";
    else if (keyWord.compare("error_mu_dec"))
        return "pmdec_error";
    else if (keyWord.compare("parallax"))
        return "parallax";
    else if (keyWord.compare("error_parallax"))
        return "parallax_error";
/*    else if (keyWord.compare(""))
        return "";
    else if (keyWord.compare(""))
        return "";
    else if (keyWord.compare(""))
        return "";*/
    else
        throw std::runtime_error("obsGetHeaderKeyWord: ERROR: unknown keyWord <"+keyWord+">");
}

unsigned getNStepsMagnitude(){
    return 10;
}

unsigned getNSims(){
    return 2;
}

string getPhotometricSystem(){
    return "UBV";//"SDSS"
}
